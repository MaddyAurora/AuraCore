Work in progress, not functional.

# AuraCore

AuraCore is a local-first Gradio WebUI that combines:

1) **Chat** with a local LLM via Ollama.
2) **Image generation** via ComfyUI (SDXL).
3) **Image editing** via a pluggable backend (Klein 4B planned; not wired yet).

## Pinokio (Windows)

This repo is set up for a simple Pinokio UX:

- Click **Install** (installs AuraCore Python deps + attempts Ollama install + installs ComfyUI into `backends/ComfyUI`).
- Click **Start** (starts Ollama + pulls `qwen2.5`, starts ComfyUI, launches AuraCore).

## Notes

- SDXL checkpoint files are downloaded separately into `backends/ComfyUI/models/checkpoints/`.
- PyTorch install attempts CUDA 12.9 wheels first (`cu129`) and falls back to `cu124` if needed.
- No license is set yet; default copyright applies.
