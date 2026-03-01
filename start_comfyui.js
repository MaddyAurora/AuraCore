module.exports = {
  daemon: true,
  run: [
    {
      method: "shell.run",
      params: {
        message: [
          "if not exist backends\\ComfyUI\\env\\Scripts\\python.exe (echo ComfyUI venv missing. Run install_comfyui.js first. & exit /b 1)",
          "backends\\ComfyUI\\env\\Scripts\\python.exe backends\\ComfyUI\\main.py --listen 127.0.0.1 --port 8188"
        ],
        on: [{
          event: "/8188/",
          done: true
        }]
      }
    },
    {
      method: "notify",
      params: {
        html: "ComfyUI started on http://127.0.0.1:8188"
      }
    }
  ]
}
