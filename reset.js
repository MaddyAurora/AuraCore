module.exports = {
  run: [
    {
      method: "shell.run",
      params: {
        message: [
          "rm -rf env __pycache__ aura_core/__pycache__ workflows/__pycache__ || true"
        ]
      }
    },
    {
      method: "notify",
      params: {
        html: "Reset complete. Re-run Install, then Start."
      }
    }
  ]
}
