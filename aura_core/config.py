from __future__ import annotations

from pydantic import BaseModel


class Settings(BaseModel):
    llm_backend: str = "ollama"
    image_gen_backend: str = "comfyui"
    image_edit_backend: str = "klein"

    ollama_host: str = "http://127.0.0.1:11434"
    ollama_model: str = "llama3.1"

    comfyui_host: str = "http://127.0.0.1:8188"
    comfyui_workflow_path: str = "workflows/comfyui_sdxl_txt2img.example.json"

    def from_env() -> "Settings":
        import os

        return Settings(
            llm_backend=os.environ.get("AURACORE_LLM_BACKEND", "ollama"),
            image_gen_backend=os.environ.get("AURACORE_IMAGE_GEN_BACKEND", "comfyui"),
            image_edit_backend=os.environ.get("AURACORE_IMAGE_EDIT_BACKEND", "klein"),
            ollama_host=os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434"),
            ollama_model=os.environ.get("OLLAMA_MODEL", "llama3.1"),
            comfyui_host=os.environ.get("COMFYUI_HOST", "http://127.0.0.1:8188"),
            comfyui_workflow_path=os.environ.get(
                "COMFYUI_WORKFLOW_PATH", "workflows/comfyui_sdxl_txt2img.example.json"
            ),
        )
