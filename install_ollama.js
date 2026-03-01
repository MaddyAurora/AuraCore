module.exports = {
  run: [
    {
      method: "shell.run",
      params: {
        message: [
          "echo Installing Ollama (Windows)...",
          "where winget >NUL 2>&1 && (winget install --id Ollama.Ollama -e --accept-package-agreements --accept-source-agreements) || (echo winget not found; please install Ollama manually from https://ollama.com/download)",
          "where ollama >NUL 2>&1 && (ollama --version) || (echo Ollama executable not found in PATH yet. If you just installed it, restart Pinokio.)"
        ]
      }
    },
    {
      method: "notify",
      params: {
        html: "Ollama install step finished. If Ollama wasn't found, install it from https://ollama.com/download then restart Pinokio."
      }
    }
  ]
}
