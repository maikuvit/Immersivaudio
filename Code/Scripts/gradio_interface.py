# pip install gradio

import gradio as gr

from main import main


# Define the interface components and structure them.
demo = gr.Interface(
    fn=main,
    inputs=[
        gr.Textbox(label="Video Path Input")  # Input component
    ],
    outputs=[
        gr.Textbox(label="Operation History", interactive=False),  # Text output
        gr.Video(label="Processed Video", interactive=False),       # Video output
        gr.Audio(label="Generated Audio", interactive=False)        # Audio output
    ]
)

# Create columns with the desired components.
column1 = gr.Column([
    gr.Textbox(label="Video Path Input"),
    gr.Textbox(label="Operation History", interactive=False)
])
column2 = gr.Column([
    gr.Video(label="Processed Video", interactive=False, height="50%"),
    gr.Audio(label="Generated Audio", interactive=False)
])

# Combine columns into a row for the layout.
layout = gr.Row([column1, column2])

demo.launch()
