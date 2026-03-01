module.exports = {
  run: [
    {
      method: "shell.run",
      params: {
        venv: "env",
        message: [
          "echo === AuraCore: install (all-in-one) ===",
          "python -m pip install --upgrade pip",
          "pip install -r requirements.txt",
          "echo.",
          "echo === Ollama: install (Windows) ===",
          "where winget >NUL 2>&1 && (winget install --id Ollama.Ollama -e --accept-package-agreements --accept-source-agreements) || (echo winget not found; please install Ollama manually from https://ollama.com/download)",
          "where ollama >NUL 2>&1 && (ollama --version) || (echo Ollama executable not found in PATH yet. If you just installed it, restart Pinokio.)",
          "echo.",
          "echo === ComfyUI: install (Windows) ===",
          "if not exist backends mkdir backends",
          "if not exist backends\\ComfyUI (git clone https://github.com/comfyanonymous/ComfyUI backends\\ComfyUI) else (echo ComfyUI already present at backends\\ComfyUI)",
          "python -m venv backends\\ComfyUI\\env",
          "backends\\ComfyUI\\env\\Scripts\\python.exe -m pip install --upgrade pip",
          "echo Installing PyTorch for CUDA 12.9 (cu129) first, then fallback to cu124 if unavailable...",
          "backends\\ComfyUI\\env\\Scripts\\python.exe -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu129 || backends\\ComfyUI\\env\\Scripts\\python.exe -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124",
          "backends\\ComfyUI\\env\\Scripts\\python.exe -m pip install -r backends\\ComfyUI\\requirements.txt",
          "echo.",
          "echo Install complete. Next: click Start."
        ]
      }
    },
    {
      method: "notify",
      params: {
        html: "Install complete. Click Start to launch AuraCore + Ollama + ComfyUI."
      }
    }
  ]
}
