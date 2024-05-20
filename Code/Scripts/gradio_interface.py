# pip install gradio

import gradio as gr

from main import main


# Define the interface components and structure them.
demo = gr.Interface(
    fn=main,
    inputs=[
        gr.Video(label="Video Path Input")  # Input component
    ],
    outputs=[
        gr.Textbox(label="Operation History", interactive=False),  # Text output
        gr.Image(label="Processed Video", interactive=False),       # Video output+
        gr.Text(label="Best Frame Description", interactive=False),
        gr.Text(label="Json complete output", interactive=False), 
    ],
    allow_flagging="never"
)

demo.launch()
