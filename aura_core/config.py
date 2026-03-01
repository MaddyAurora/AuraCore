from __future__ import annotations

from pydantic import BaseModel


class Settings(BaseModel):
    llm_backend: str = "ollama"
    image_gen_backend: str = "comfyui"
    image_edit_backend: str = "klein"

    system_prompt: str = ""

    ollama_host: str = "http://127.0.0.1:11434"
    ollama_model: str = "llama3.1"

    comfyui_host: str = "http://127.0.0.1:8188"

    sdxl_model: str = "sd_xl_base_1.0.safetensors"
    sdxl_sampler: str = "euler"
    sdxl_scheduler: str = "normal"
    sdxl_width: int = 1024
    sdxl_height: int = 1024

    @classmethod
    def from_env(cls) -> "Settings":
        import os

        return cls(
            llm_backend=os.environ.get("AURACORE_LLM_BACKEND", "ollama"),
            image_gen_backend=os.environ.get("AURACORE_IMAGE_GEN_BACKEND", "comfyui"),
            image_edit_backend=os.environ.get("AURACORE_IMAGE_EDIT_BACKEND", "klein"),
            system_prompt=os.environ.get("AURACORE_SYSTEM_PROMPT", ""),
            ollama_host=os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434"),
            ollama_model=os.environ.get("OLLAMA_MODEL", "llama3.1"),
            comfyui_host=os.environ.get("COMFYUI_HOST", "http://127.0.0.1:8188"),
            sdxl_model=os.environ.get("AURACORE_SDXL_MODEL", "sd_xl_base_1.0.safetensors"),
            sdxl_sampler=os.environ.get("AURACORE_SDXL_SAMPLER", "euler"),
            sdxl_scheduler=os.environ.get("AURACORE_SDXL_SCHEDULER", "normal"),
            sdxl_width=int(os.environ.get("AURACORE_SDXL_WIDTH", "1024")),
            sdxl_height=int(os.environ.get("AURACORE_SDXL_HEIGHT", "1024")),
        )
