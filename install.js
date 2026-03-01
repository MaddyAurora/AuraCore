module.exports = {
  run: [
    {
      method: "shell.run",
      params: {
        venv: "env",
        message: [
          "pip install -r requirements.txt"
        ]
      }
    },
    {
      method: "notify",
      params: {
        html: "Install complete. Click the Start tab to launch AuraCore."
      }
    }
  ]
}
