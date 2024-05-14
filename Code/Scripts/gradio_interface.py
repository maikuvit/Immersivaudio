# pip install gradio

import gradio as gr

from main import main

demo = gr.Interface(
    fn=main,
    inputs=["video"],
    outputs=[gr.Text(label="Frames extraction."), gr.Image(label="Best frame selected."), gr.Text(label="Best frame description.")],
    allow_flagging="never"
)

demo.launch()
