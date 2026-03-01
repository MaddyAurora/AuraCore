from __future__ import annotations

import time
import uuid
import random
from io import BytesIO
from typing import Optional, Tuple, List

import requests
from PIL import Image


class ComfyUIImageGenBackend:
    def __init__(self, host: str):
        self.host = host.rstrip("/")
        self.client_id = str(uuid.uuid4())

    def get_options(
        self,
        current_model: Optional[str] = None,
        current_sampler: Optional[str] = None,
        current_scheduler: Optional[str] = None,
    ) -> Tuple[List[str], List[str], List[str], str]:
        try:
            info = requests.get(f"{self.host}/object_info", timeout=10).json()
        except Exception as e:
            models = [current_model] if current_model else []
            samplers = [current_sampler] if current_sampler else []
            schedulers = [current_scheduler] if current_scheduler else []
            return models, samplers, schedulers, f"Couldn't query /object_info from ComfyUI ({self.host}). Error: {e}"

        def _values(node_class: str, field: str) -> List[str]:
            try:
                required = (info.get(node_class) or {}).get("input") or {}
                required = required.get("required") or {}
                entry = required.get(field)
                if not entry:
                    return []
                vals = entry[0]
                if isinstance(vals, list):
                    return [str(v) for v in vals]
            except Exception:
                return []
            return []

        models = _values("CheckpointLoaderSimple", "ckpt_name")
        samplers = _values("KSampler", "sampler_name")
        schedulers = _values("KSampler", "scheduler")

        note = "Fetched options from ComfyUI /object_info."
        return models, samplers, schedulers, note

    def generate(
        self,
        prompt: str,
        model: str,
        sampler: str,
        scheduler: str,
        width: int,
        height: int,
        negative_prompt: str = "text, watermark",
        steps: int = 25,
        cfg: float = 8.0,
        timeout_s: int = 300,
    ) -> tuple[Optional[Image.Image], str]:
        try:
            r = requests.get(f"{self.host}/system_stats", timeout=5)
            r.raise_for_status()
        except Exception as e:
            return None, f"Couldn't reach ComfyUI at {self.host}. Start ComfyUI first. Error: {e}"

        seed = random.randint(1, 2**31 - 1)

        prompt_graph = {
            "3": {
                "class_type": "CheckpointLoaderSimple",
                "inputs": {"ckpt_name": model},
            },
            "4": {
                "class_type": "CLIPTextEncode",
                "inputs": {"text": prompt, "clip": ["3", 1]},
            },
            "5": {
                "class_type": "CLIPTextEncode",
                "inputs": {"text": negative_prompt, "clip": ["3", 1]},
            },
            "6": {
                "class_type": "EmptyLatentImage",
                "inputs": {"width": int(width), "height": int(height), "batch_size": 1},
            },
            "7": {
                "class_type": "KSampler",
                "inputs": {
                    "seed": seed,
                    "steps": int(steps),
                    "cfg": float(cfg),
                    "sampler_name": sampler,
                    "scheduler": scheduler,
                    "denoise": 1.0,
                    "model": ["3", 0],
                    "positive": ["4", 0],
                    "negative": ["5", 0],
                    "latent_image": ["6", 0],
                },
            },
            "8": {
                "class_type": "VAEDecode",
                "inputs": {"samples": ["7", 0], "vae": ["3", 2]},
            },
            "9": {
                "class_type": "SaveImage",
                "inputs": {"filename_prefix": "AuraCoreOutput", "images": ["8", 0]},
            },
        }

        try:
            submit = requests.post(
                f"{self.host}/prompt",
                json={"prompt": prompt_graph, "client_id": self.client_id},
                timeout=30,
            )
            submit.raise_for_status()
            prompt_id = submit.json().get("prompt_id")
            if not prompt_id:
                return None, f"ComfyUI /prompt did not return prompt_id. Response: {submit.text}"
        except Exception as e:
            return None, f"Failed to submit prompt to ComfyUI /prompt. Error: {e}"

        start = time.time()
        while True:
            if time.time() - start > timeout_s:
                return None, f"Timed out waiting for ComfyUI job (prompt_id={prompt_id})."

            try:
                hist = requests.get(f"{self.host}/history/{prompt_id}", timeout=15)
                hist.raise_for_status()
                data = hist.json() or {}
            except Exception:
                time.sleep(0.5)
                continue

            item = data.get(str(prompt_id)) or data.get(prompt_id)
            if not item:
                time.sleep(0.5)
                continue

            outputs = item.get("outputs") or {}
            save_node = outputs.get("9") or outputs.get(9)
            if not save_node:
                time.sleep(0.5)
                continue

            images = save_node.get("images") or []
            if not images:
                time.sleep(0.5)
                continue

            img0 = images[0]
            filename = img0.get("filename")
            subfolder = img0.get("subfolder") or ""
            ftype = img0.get("type") or "output"
            if not filename:
                return None, "ComfyUI returned an image entry without filename."

            try:
                view = requests.get(
                    f"{self.host}/view",
                    params={"filename": filename, "subfolder": subfolder, "type": ftype},
                    timeout=60,
                )
                view.raise_for_status()
                img = Image.open(BytesIO(view.content)).convert("RGB")
                note = (
                    f"ComfyUI OK. model={model}, sampler={sampler}, scheduler={scheduler}, "
                    f"{width}x{height}, seed={seed}"
                )
                return img, note
            except Exception as e:
                return None, f"Failed to download image via ComfyUI /view. Error: {e}"
