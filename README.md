# AuraCore

AuraCore is a local-first Gradio WebUI that combines:

1) **Chat** with a local LLM via Ollama (history + optional lightweight “memory”).
2) **Image generation** via a pluggable backend (recommended: ComfyUI for SDXL).
3) **Image editing** via a pluggable backend (planned: FLUX.2 klein 4B / “Klein 4B”).

This repository is structured to be “Pinokio-friendly” and includes one-click scripts to install and start the required backends.

## Quickstart (Pinokio / Windows)

1) Install AuraCore: run `Install (AuraCore)`.
2) Install backends:
- Run `install_ollama.js` (or install Ollama manually if winget is unavailable).
- Run `install_comfyui.js` (installs ComfyUI into `backends/ComfyUI` and installs GPU PyTorch).
3) Download SDXL model(s):
- Set environment variables in Pinokio before running `Download Models`:
- `SDXL_CHECKPOINT_URL` = direct download URL
- `SDXL_CHECKPOINT_FILENAME` = e.g. `sd_xl_base_1.0.safetensors`
4) Start everything: run `Start (All)`.

## Defaults

- Ollama host: `http://127.0.0.1:11434`
- Ollama model: `qwen2.5`
- ComfyUI host: `http://127.0.0.1:8188`

## Backends (pluggable)

AuraCore selects backends via environment variables (or `.env`):

- `AURACORE_LLM_BACKEND=ollama`
- `AURACORE_IMAGE_GEN_BACKEND=comfyui`
- `AURACORE_IMAGE_EDIT_BACKEND=klein`

And endpoints:

- `OLLAMA_HOST=http://127.0.0.1:11434`
- `COMFYUI_HOST=http://127.0.0.1:8188`

## Notes

- No license is set yet; default copyright applies.
- Klein 4B image editing is not wired yet.
