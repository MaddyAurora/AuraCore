module.exports = {
  run: [
    {
      method: "shell.run",
      params: {
        message: [
          "echo Installing backends...",
          "node -v >NUL 2>&1 || echo (Note: node not found, continuing anyway)",
          "echo Step 1/2: Ollama",
          "echo (Run install_ollama.js if you need to install Ollama)",
          "echo Step 2/2: ComfyUI",
          "echo (Run install_comfyui.js to install ComfyUI in backends\\ComfyUI)",
          "echo Done."
        ]
      }
    },
    {
      method: "notify",
      params: {
        html: "Backends overview: run install_ollama.js (Ollama) and install_comfyui.js (ComfyUI)."
      }
    }
  ]
}
