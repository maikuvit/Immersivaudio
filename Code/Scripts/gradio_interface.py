# pip install gradio

import gradio as gr

from main import main

def main(video_path):
    print(video_path)


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
        gr.Image(label="Image Input")  # Input component
    ],
    outputs=[
        gr.Image(label="Processed Video", interactive=False),       # Video output
        gr.Text(label="Generated audio", interactive=False),
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