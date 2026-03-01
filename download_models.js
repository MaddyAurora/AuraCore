module.exports = {
  run: [
    {
      method: "shell.run",
      params: {
        message: [
          "echo Downloading models...",
          "if not exist backends\\ComfyUI (echo ComfyUI not installed. Run install_comfyui.js first. & exit /b 1)",
          "if not exist backends\\ComfyUI\\models\\checkpoints mkdir backends\\ComfyUI\\models\\checkpoints",
          "if \"%SDXL_CHECKPOINT_URL%\"==\"\" (echo Set SDXL_CHECKPOINT_URL to a direct download link. & exit /b 1)",
          "if \"%SDXL_CHECKPOINT_FILENAME%\"==\"\" (echo Set SDXL_CHECKPOINT_FILENAME e.g. my_sdxl.safetensors. & exit /b 1)",
          "powershell -NoProfile -ExecutionPolicy Bypass -Command \"$u=$env:SDXL_CHECKPOINT_URL; $o='backends\\ComfyUI\\models\\checkpoints\\'+$env:SDXL_CHECKPOINT_FILENAME; Write-Host ('Downloading '+$u+' -> '+$o); Invoke-WebRequest -Uri $u -OutFile $o\""
        ]
      }
    },
    {
      method: "notify",
      params: {
        html: "Model download finished (if no errors). You can now select the checkpoint in AuraCore Settings and generate."
      }
    }
  ]
}
