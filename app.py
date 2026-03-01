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
        state = gr.State(settings.model_dump(), render=False)

        gr.Markdown(
            "# AuraCore\nLocal-first chat + SDXL (ComfyUI) + image editing (Klein 4B) — pluggable backends"
        )

        with gr.Tabs():
            with gr.TabItem("Chat"):
                chat = gr.Chatbot(height=480)
                msg = gr.Textbox(label="Message", placeholder="Talk to your local assistant…")
                with gr.Row():
                    send = gr.Button("Send")
                    clear = gr.Button("Clear")

                status = gr.Markdown("")

                def _send(message, history, st):
                    history = history or []
                    reply, note = agent.chat(message, history, system_prompt=st.get("system_prompt", ""))
                    history = history + [(message, reply)]
                    return history, "", (note or "")

                send.click(_send, inputs=[msg, chat, state], outputs=[chat, msg, status])
                msg.submit(_send, inputs=[msg, chat, state], outputs=[chat, msg, status])
                clear.click(lambda: ([], ""), outputs=[chat, status])

            with gr.TabItem("Generate"):
                gen_prompt = gr.Textbox(label="Prompt", placeholder="Describe the image…")
                gen_btn = gr.Button("Generate")
                gen_out = gr.Image(label="Output", type="pil")
                gen_status = gr.Markdown("")

                def _gen(prompt, st):
                    img, note = agent.generate_image(
                        prompt,
                        model=st.get("sdxl_model"),
                        sampler=st.get("sdxl_sampler"),
                        scheduler=st.get("sdxl_scheduler"),
                        width=int(st.get("sdxl_width", 1024)),
                        height=int(st.get("sdxl_height", 1024)),
                    )
                    return img, (note or "")

                gen_btn.click(_gen, inputs=[gen_prompt, state], outputs=[gen_out, gen_status])

            with gr.TabItem("Edit"):
                edit_in = gr.Image(label="Input image", type="pil")
                edit_prompt = gr.Textbox(label="Edit request", placeholder="What should change?")
                edit_btn = gr.Button("Edit")
                edit_out = gr.Image(label="Output", type="pil")
                edit_status = gr.Markdown("")

                def _edit(img: Image.Image, prompt: str, st):
                    out, note = agent.edit_image(img, prompt)
                    return out, (note or "")

                edit_btn.click(
                    _edit, inputs=[edit_in, edit_prompt, state], outputs=[edit_out, edit_status]
                )

            with gr.TabItem("Settings"):
                gr.Markdown("### ComfyUI (SDXL) generation")

                with gr.Row():
                    sdxl_model = gr.Dropdown(
                        label="SDXL checkpoint",
                        choices=[settings.sdxl_model] if settings.sdxl_model else [],
                        value=settings.sdxl_model,
                        allow_custom_value=True,
                    )
                    refresh = gr.Button("Refresh from ComfyUI")

                with gr.Row():
                    sampler = gr.Dropdown(
                        label="Sampler",
                        choices=[settings.sdxl_sampler] if settings.sdxl_sampler else [],
                        value=settings.sdxl_sampler,
                        allow_custom_value=True,
                    )
                    scheduler = gr.Dropdown(
                        label="Scheduler",
                        choices=[settings.sdxl_scheduler] if settings.sdxl_scheduler else [],
                        value=settings.sdxl_scheduler,
                        allow_custom_value=True,
                    )

                with gr.Row():
                    width = gr.Number(label="Width", value=settings.sdxl_width, precision=0)
                    height = gr.Number(label="Height", value=settings.sdxl_height, precision=0)

                apply_btn = gr.Button("Apply")

                gr.Markdown("### Current runtime settings")
                current = gr.JSON(settings.model_dump())

                gr.Markdown("### System prompt")
                system_prompt = gr.Textbox(
                    label="System prompt (applies to chat)",
                    value=settings.system_prompt,
                    lines=8,
                    placeholder="You are AuraCore…",
                )

                def _apply(model, sampler_v, scheduler_v, w, h, sys_prompt, st):
                    st = dict(st or {})
                    st["sdxl_model"] = model
                    st["sdxl_sampler"] = sampler_v
                    st["sdxl_scheduler"] = scheduler_v
                    st["sdxl_width"] = int(w or 1024)
                    st["sdxl_height"] = int(h or 1024)
                    st["system_prompt"] = sys_prompt or ""
                    return st, st

                apply_btn.click(
                    _apply,
                    inputs=[sdxl_model, sampler, scheduler, width, height, system_prompt, state],
                    outputs=[state, current],
                )

                def _refresh(st):
                    st = dict(st or {})
                    models, samplers, schedulers, note = agent.image_gen_options(
                        current_model=st.get("sdxl_model"),
                        current_sampler=st.get("sdxl_sampler"),
                        current_scheduler=st.get("sdxl_scheduler"),
                    )
                    return (
                        gr.update(
                            choices=models,
                            value=st.get("sdxl_model") or (models[0] if models else None),
                        ),
                        gr.update(
                            choices=samplers,
                            value=st.get("sdxl_sampler") or (samplers[0] if samplers else None),
                        ),
                        gr.update(
                            choices=schedulers,
                            value=st.get("sdxl_scheduler") or (schedulers[0] if schedulers else None),
                        ),
                        note,
                    )

                refresh_status = gr.Markdown("")
                refresh.click(
                    _refresh,
                    inputs=[state],
                    outputs=[sdxl_model, sampler, scheduler, refresh_status],
                )

    return demo


if __name__ == "__main__":
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", "7860"))
    app = build_app()
    app.launch(server_name=host, server_port=port)
