import os

from dotenv import load_dotenv

load_dotenv()

import gradio as gr
from PIL import Image

from aura_core.agent import AuraCoreAgent
from aura_core.config import Settings


def build_app():
    settings = Settings.from_env()
    agent = AuraCoreAgent(settings)

    with gr.Blocks(title="AuraCore") as demo:
        gr.Markdown("# AuraCore\nLocal-first chat + SDXL (ComfyUI) + image editing (Klein 4B) — pluggable backends")

        with gr.Tabs():
            with gr.TabItem("Chat"):
                chat = gr.Chatbot(height=480)
                msg = gr.Textbox(label="Message", placeholder="Talk to your local assistant…")
                with gr.Row():
                    send = gr.Button("Send")
                    clear = gr.Button("Clear")

                status = gr.Markdown("")

                def _send(message, history):
                    history = history or []
                    reply, note = agent.chat(message, history)
                    history = history + [(message, reply)]
                    return history, "", (note or "")

                send.click(_send, inputs=[msg, chat], outputs=[chat, msg, status])
                msg.submit(_send, inputs=[msg, chat], outputs=[chat, msg, status])
                clear.click(lambda: ([], ""), outputs=[chat, status])

            with gr.TabItem("Generate"):
                gen_prompt = gr.Textbox(label="Prompt", placeholder="Describe the image…")
                gen_btn = gr.Button("Generate")
                gen_out = gr.Image(label="Output", type="pil")
                gen_status = gr.Markdown("")

                def _gen(prompt):
                    img, note = agent.generate_image(prompt)
                    return img, (note or "")

                gen_btn.click(_gen, inputs=[gen_prompt], outputs=[gen_out, gen_status])

            with gr.TabItem("Edit"):
                edit_in = gr.Image(label="Input image", type="pil")
                edit_prompt = gr.Textbox(label="Edit request", placeholder="What should change?")
                edit_btn = gr.Button("Edit")
                edit_out = gr.Image(label="Output", type="pil")
                edit_status = gr.Markdown("")

                def _edit(img: Image.Image, prompt: str):
                    out, note = agent.edit_image(img, prompt)
                    return out, (note or "")

                edit_btn.click(_edit, inputs=[edit_in, edit_prompt], outputs=[edit_out, edit_status])

            with gr.TabItem("Settings"):
                gr.Markdown("### Current settings")
                gr.JSON(settings.model_dump())
                gr.Markdown("Edit environment variables (or .env) and restart the app to change backends/endpoints.")

    return demo


if __name__ == "__main__":
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", "7860"))
    app = build_app()
    app.launch(server_name=host, server_port=port)
