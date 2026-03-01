from __future__ import annotations

from typing import List, Tuple, Optional

from PIL import Image

from aura_core.config import Settings
from aura_core.backends.base import (
    BaseLLMBackend,
    BaseImageGenBackend,
    BaseImageEditBackend,
)
from aura_core.backends.llm_ollama import OllamaLLMBackend
from aura_core.backends.imagegen_comfyui import ComfyUIImageGenBackend
from aura_core.backends.imageedit_klein import KleinImageEditBackend


class AuraCoreAgent:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.llm: BaseLLMBackend = self._make_llm()
        self.image_gen: BaseImageGenBackend = self._make_image_gen()
        self.image_edit: BaseImageEditBackend = self._make_image_edit()

    def _make_llm(self) -> BaseLLMBackend:
        if self.settings.llm_backend == "ollama":
            return OllamaLLMBackend(self.settings.ollama_host, self.settings.ollama_model)
        raise ValueError(f"Unknown LLM backend: {self.settings.llm_backend}")

    def _make_image_gen(self) -> BaseImageGenBackend:
        if self.settings.image_gen_backend == "comfyui":
            return ComfyUIImageGenBackend(
                host=self.settings.comfyui_host,
                workflow_path=self.settings.comfyui_workflow_path,
            )
        raise ValueError(f"Unknown image gen backend: {self.settings.image_gen_backend}")

    def _make_image_edit(self) -> BaseImageEditBackend:
        if self.settings.image_edit_backend == "klein":
            return KleinImageEditBackend()
        raise ValueError(f"Unknown image edit backend: {self.settings.image_edit_backend}")

    def chat(self, message: str, history: List[Tuple[str, str]]):
        if not message:
            return "", ""

        routed = self._maybe_route_tool(message)
        if routed is not None:
            return routed

        reply = self.llm.chat(message, history)
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

    def generate_image(self, prompt: str):
        return self.image_gen.generate(prompt)

    def edit_image(self, image: Image.Image, prompt: str):
        return self.image_edit.edit(image, prompt)
