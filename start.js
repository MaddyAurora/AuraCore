module.exports = {
  daemon: true,
  run: [
    {
      method: "shell.run",
      params: {
        venv: "env",
        env: {
          HOST: "127.0.0.1",
          PORT: "7860",
          OLLAMA_HOST: "http://127.0.0.1:11434",
          OLLAMA_MODEL: "qwen2.5",
          COMFYUI_HOST: "http://127.0.0.1:8188"
        },
        message: [
          "echo === Starting Ollama (if installed) ===",
          "where ollama >NUL 2>&1 && (cmd /c start \"\" /B ollama serve) || (echo Ollama not found; install it from https://ollama.com/download)",
          "where ollama >NUL 2>&1 && (ollama pull qwen2.5) || (echo Skipping model pull because Ollama is missing)",
          "echo.",
          "echo === Starting ComfyUI (if installed) ===",
          "if exist backends\\ComfyUI\\env\\Scripts\\python.exe (cmd /c start \"\" /B backends\\ComfyUI\\env\\Scripts\\python.exe backends\\ComfyUI\\main.py --listen 127.0.0.1 --port 8188) else (echo ComfyUI not installed; run Install first)",
          "echo.",
          "echo === Starting AuraCore ===",
          "python app.py"
        ],
        on: [{
          event: "/http:\\/\\/\\/\\S+/",
          done: true
        }]
      }
    },
    {
      method: "local.set",
      params: {
        url: "{{input.event[0]}}"
      }
    }
  ]
}
