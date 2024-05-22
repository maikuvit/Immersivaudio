# pip install gradio

import gradio as gr

from main import main

# Interface title and description
interface_title = "Immersivaudio AI Video and Image Enhancer"
interface_description = "This interface allows you to enhance your videos and images with AI-generated audio. You can upload a video or an image and the AI will generate audio based on the content of the input. Project made by Daniele Avolio, Michele Vitale, Theo ___"


# Define the interface components and structure them.
video_interface = gr.Interface(
    fn=main,
    title=interface_title,
    description=interface_description,
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