# AuraCore

AuraCore is a local-first Gradio WebUI that combines:

1) **Chat** with a local LLM via Ollama (history + optional lightweight “memory”).
2) **Image generation** via a pluggable backend (recommended: ComfyUI for SDXL).
3) **Image editing** via a pluggable backend (planned: FLUX.2 klein 4B / “Klein 4B”).

This repository is structured to be “Pinokio-friendly” (install/start scripts included).

## Quickstart (Pinokio)

1. Install Pinokio.
2. Put/clone this repo under `PINOKIO_HOME/api/AuraCore` (or install from URL in Pinokio).
3. Click `install.js`, then `start.js`.

Pinokio will create a local venv at `env/` and run the app in daemon mode.

## Quickstart (manual)

```bash
python -m venv env
# Windows: env\Scripts\activate
# macOS/Linux: source env/bin/activate
pip install -r requirements.txt
python app.py
```

Open the URL printed in the console.

## Backends (pluggable)

AuraCore selects backends via environment variables (or `.env`):

- `AURACORE_LLM_BACKEND=ollama`
- `AURACORE_IMAGE_GEN_BACKEND=comfyui`
- `AURACORE_IMAGE_EDIT_BACKEND=klein`

And endpoints:

- `OLLAMA_HOST=http://127.0.0.1:11434`
- `COMFYUI_HOST=http://127.0.0.1:8188`

### Ollama

Run Ollama separately and ensure your model is pulled.

### ComfyUI (SDXL)

Run ComfyUI separately (with an SDXL workflow available). AuraCore includes an example workflow JSON under `workflows/` that you can adapt.

## Project layout

- `app.py`: Gradio UI (chat + generate + edit)
- `aura_core/`: core logic, backend interfaces, adapters
- `install.js`, `start.js`, `pinokio.js`: Pinokio launcher scripts

## Notes

- No license is set yet; default copyright applies.
- First milestone is a reliable local chat + backend wiring + minimal tool-routing.
