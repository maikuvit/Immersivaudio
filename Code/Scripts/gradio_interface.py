# pip install gradio

import gradio as gr

from main import main



demo = gr.Interface(
    fn=main,
    inputs=["text"],
    outputs=["text"],
)

demo.launch()
