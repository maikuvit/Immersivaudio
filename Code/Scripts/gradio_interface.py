# pip install gradio

import gradio as gr

from main import main

# Define the interface components and structure them.
video_interface = gr.Interface(
    fn=main,
    inputs=[
        gr.Video(label="Video Path Input")  # Input component
    ],
    outputs=[
        gr.Video(label="Processed Video", interactive=False),       # Video output
        gr.Audio(label="Generated audio", interactive=False),
        gr.Text(label="Used prompt", interactive = False),
        gr.Text(label="Json complete output", interactive=False), 
    ],
    allow_flagging="never"
)

image_interface = gr.Interface(
    fn=main,
    inputs=[
        gr.Image(label="Image Input", type="filepath"),  # Input component
        gr.Slider(label="Duration", minimum=1, maximum=120, step=1)
    ],
    outputs=[
        gr.Video(label="Processed Video", interactive=False),       # Video output
        gr.Audio(label="Generated audio", interactive=False),
        gr.Text(label="Used prompt", interactive = False),
        gr.Text(label="Json complete output", interactive=False), 
    ],
    allow_flagging="never"
)

# Use both interfaces
demo = gr.TabbedInterface(
    [
        video_interface, image_interface
    ],
    tab_names=["Video", "Image"]
)

# Launch the interface
demo.launch(share=True)