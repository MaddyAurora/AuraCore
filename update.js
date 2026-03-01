module.exports = {
  run: [
    {
      method: "shell.run",
      params: {
        message: [
          "git pull"
        ]
      }
    },
    {
      method: "notify",
      params: {
        html: "Update complete. If dependencies changed, re-run Install."
      }
    }
  ]
}
