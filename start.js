module.exports = {
  daemon: true,
  run: [
    {
      method: "shell.run",
      params: {
        venv: "env",
        env: {
          HOST: "127.0.0.1",
          PORT: "7860"
        },
        message: [
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
