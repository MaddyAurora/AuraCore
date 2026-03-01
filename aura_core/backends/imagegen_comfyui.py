from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

import requests
from PIL import Image


class ComfyUIImageGenBackend:
    def __init__(self, host: str, workflow_path: str):
        self.host = host.rstrip("/")
        self.workflow_path = workflow_path

    def generate(self, prompt: str) -> tuple[Optional[Image.Image], str]:
        wf_path = Path(self.workflow_path)
        if not wf_path.exists():
            return None, f"Workflow not found: {wf_path}. Configure COMFYUI_WORKFLOW_PATH."

        try:
            workflow = json.loads(wf_path.read_text(encoding="utf-8"))
        except Exception as e:
            return None, f"Failed to read workflow JSON: {e}"

        note = (
            "ComfyUI integration is scaffolded. You must adapt the workflow JSON to your ComfyUI setup "
            "and ensure the prompt node is mapped."
        )

        try:
            r = requests.get(f"{self.host}/system_stats", timeout=5)
            r.raise_for_status()
        except Exception as e:
            return None, f"Couldn't reach ComfyUI at {self.host}. Start ComfyUI first. Error: {e}"

        return None, note
