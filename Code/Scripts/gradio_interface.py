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
        gr.Video(label="Processed Video", interactive=False),       # Video output+
        gr.Audio(label="Generated audio", interactive=False),
        gr.Text(label="Used prompt", interactive = False),
        gr.Text(label="Json complete output", interactive=False), 
    ],
    allow_flagging="never"
)

demo.launch(share=True)
