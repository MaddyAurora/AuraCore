module.exports = {
  run: [
    {
      method: "shell.run",
      params: {
        message: [
          "where ollama >NUL 2>&1 || (echo Ollama not found. Run install_ollama.js first. & exit /b 1)",
          "ollama pull qwen2.5"
        ]
      }
    },
    {
      method: "notify",
      params: {
        html: "Ollama model pulled: qwen2.5"
      }
    }
  ]
}
