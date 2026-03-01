module.exports = {
  run: [
    {
      method: "shell.run",
      params: {
        message: [
          "echo Installing ComfyUI (Windows)...",
          "if not exist backends mkdir backends",
          "if not exist backends\\ComfyUI (git clone https://github.com/comfyanonymous/ComfyUI backends\\ComfyUI) else (echo ComfyUI already present at backends\\ComfyUI)",
          "echo Creating ComfyUI venv at backends\\ComfyUI\\env",
          "python -m venv backends\\ComfyUI\\env",
          "backends\\ComfyUI\\env\\Scripts\\python.exe -m pip install --upgrade pip",
          "echo Installing PyTorch for CUDA 12.9 (cu129) first, then fallback to cu124 if unavailable...",
          "backends\\ComfyUI\\env\\Scripts\\python.exe -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu129 || backends\\ComfyUI\\env\\Scripts\\python.exe -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124",
          "backends\\ComfyUI\\env\\Scripts\\python.exe -m pip install -r backends\\ComfyUI\\requirements.txt"
        ]
      }
    },
    {
      method: "notify",
      params: {
        html: "ComfyUI install step finished. Next: use 'Download Models' to add SDXL checkpoints, then 'Start (All)' or 'Start (ComfyUI)'."
      }
    }
  ]
}
