module.exports = {
  daemon: true,
  run: [
    {
      method: "shell.run",
      params: {
        message: [
          "where ollama >NUL 2>&1 || (echo Ollama not found. Run install_ollama.js or install from https://ollama.com/download & exit /b 1)",
          "ollama serve"
        ],
        on: [{
          event: "/11434/",
          done: true
        }]
      }
    }
  ]
}
