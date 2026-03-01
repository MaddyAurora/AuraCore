from __future__ import annotations

from typing import List, Tuple, Optional

from PIL import Image

from aura_core.config import Settings
from aura_core.backends.llm_ollama import OllamaLLMBackend
from aura_core.backends.imagegen_comfyui import ComfyUIImageGenBackend
from aura_core.backends.imageedit_klein import KleinImageEditBackend


class AuraCoreAgent:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.llm = self._make_llm()
        self.image_gen = self._make_image_gen()
        self.image_edit = self._make_image_edit()

    def _make_llm(self):
        if self.settings.llm_backend == "ollama":
            return OllamaLLMBackend(self.settings.ollama_host, self.settings.ollama_model)
        raise ValueError(f"Unknown LLM backend: {self.settings.llm_backend}")

    def _make_image_gen(self):
        if self.settings.image_gen_backend == "comfyui":
            return ComfyUIImageGenBackend(host=self.settings.comfyui_host)
        raise ValueError(f"Unknown image gen backend: {self.settings.image_gen_backend}")

    def _make_image_edit(self):
        if self.settings.image_edit_backend == "klein":
            return KleinImageEditBackend()
        raise ValueError(f"Unknown image edit backend: {self.settings.image_edit_backend}")

    def chat(
        self,
        message: str,
        history: List[Tuple[str, str]],
        system_prompt: str = "",
    ):
        if not message:
            return "", ""

        routed = self._maybe_route_tool(message)
        if routed is not None:
            return routed

        reply = self.llm.chat(message, history, system_prompt=system_prompt)
        return reply, ""

    def _maybe_route_tool(self, message: str) -> Optional[tuple[str, str]]:
        m = message.lower().strip()

        if m.startswith("/img ") or "generate an image" in m or "make an image" in m:
            prompt = message[5:] if m.startswith("/img ") else message
            img, note = self.generate_image(prompt)
            if img is None:
                return f"I couldn't generate an image yet. {note}", note
            return f"Generated an image. (See the Generate tab output.) {note}", note

        if m.startswith("/edit ") or m.startswith("edit "):
            return (
                "To edit an image, go to the Edit tab, upload an image, and describe what you want changed.",
                "",
            )

        return None

    def generate_image(
        self,
        prompt: str,
        model: Optional[str] = None,
        sampler: Optional[str] = None,
        scheduler: Optional[str] = None,
        width: int = 1024,
        height: int = 1024,
    ):
        return self.image_gen.generate(
            prompt,
            model=model or self.settings.sdxl_model,
            sampler=sampler or self.settings.sdxl_sampler,
            scheduler=scheduler or self.settings.sdxl_scheduler,
            width=width or self.settings.sdxl_width,
            height=height or self.settings.sdxl_height,
        )

    def edit_image(self, image: Image.Image, prompt: str):
        return self.image_edit.edit(image, prompt)

    def image_gen_options(
        self,
        current_model: Optional[str] = None,
        current_sampler: Optional[str] = None,
        current_scheduler: Optional[str] = None,
    ):
        return self.image_gen.get_options(
            current_model=current_model,
            current_sampler=current_sampler,
            current_scheduler=current_scheduler,
        )
