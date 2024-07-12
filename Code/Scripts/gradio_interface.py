# pip install gradio

import gradio as gr

from main import main

# Interface title and description
interface_title = "Immersivaudio AI Video and Image Enhancer"
interface_description = "This interface allows you to enhance your videos and images with AI-generated audio. You can upload a video or an image and the AI will generate audio based on the content of the input. Project made by Daniele Avolio, Michele Vitale, Teodor Chakarov for the Learning Based Multimedia Processing course at Instituto Superior Tecnico, Lisbon."


# Add a callback function to toggle the visibility of the slider
def toggle_slider(checkbox_val):
    return gr.Slider(
        label="Sounds volume", minimum=0.1, maximum=1.0, value=0.5, visible=checkbox_val
    )


# Using this to debug
def dummy_function(video_path):
    return video_path


# Define the interface components and structure them.
video_interface = gr.Interface(
    fn= main,
    # fn=dummy_function,
    title=interface_title,
    description=interface_description,
    inputs=[
        gr.Video(label="Video Path Input"),  # Input component
        gr.Checkbox(label="Generate sounds"),
        gr.Number(label="Duration", minimum=1, maximum=300, value=10, visible=False),
        gr.Slider(
            label="Music Volume", minimum=0.1, maximum=1.0, value=0.5, visible=True
        ),
        gr.Slider(
            label="Sounds volume", minimum=0.1, maximum=1.0, value=0.5, visible=False
        ),
    ],
    outputs=[
        gr.Video(label="Processed Video", interactive=False),  # Video output
        gr.Audio(label="Generated audio", interactive=False),
        gr.Text(label="Used prompt", interactive=False),
        gr.Text(label="Json complete output", interactive=False),
    ],
    allow_flagging="never",
)

image_interface = gr.Interface(
    fn=main,
    # fn=dummy_function,
    title=interface_title,
    description=interface_description,
    inputs=[
        gr.Image(label="Image Input", type="filepath"),  # Input component
        gr.Checkbox(label="Generate sounds"),
        gr.Number(label="Duration", minimum=1, maximum=300, value=5),
        gr.Slider(
            label="Music Volume", minimum=0.1, maximum=1.0, value=0.5, visible=True
        ),
        gr.Slider(
            label="Sounds volume", minimum=0.1, maximum=1.0, value=0.5, visible=False
        ),
    ],
    outputs=[
        gr.Video(label="Processed Video", interactive=False),  # Video output
        gr.Audio(label="Generated audio", interactive=False),
        gr.Text(label="Used prompt", interactive=False),
        gr.Text(label="Json complete output", interactive=False),
    ],
    allow_flagging="never",
)

with image_interface as i:
    i.input_components[1].change(
        fn=toggle_slider,
        inputs=[i.input_components[1]],
        outputs=[i.input_components[4]],
    )

with video_interface as i:
    i.input_components[1].change(
        fn=toggle_slider,
        inputs=[i.input_components[1]],
        outputs=[i.input_components[4]],
    )


# Use both interfaces
demo = gr.TabbedInterface(
    [video_interface, image_interface],
    tab_names=["Video", "Image"],
    theme=gr.themes.Soft(
        primary_hue="violet",
        neutral_hue="slate",
    ),
)


# Launch the interface
demo.launch(share=True)
