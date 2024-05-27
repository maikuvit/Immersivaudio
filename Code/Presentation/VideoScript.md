# Immersivaudio - Audio generation from video features

Initial part:

Nowadays we know that AI is the main focus of the industry, and it is being used in many different ways. From text generation, like CHATGPT to image generation, like DALL-E or Stable Diffusion. 
What about audio generation? There are some models that can generate audio, but they are not as popular as the other models.
Since we all love music, we wanted to create an application that could generate music from a video, to enhance the viewer experience 
and boost the creativity of the content creators.

Of course, this is not something simple and not something trivial. We had to think about how to handle the process in a way that would be efficient and effective.

The first idea we had was to analyze the entire video and to kind of get the entire context of it. It was not actually possible and we didn't even bother to go too deep into it.
The workflow is split among 6 modules, each one with a specific task:

1. We analyze and extract a specific number of frame computed from the video length [Frame extraction]
2. We do object detection on each frame and get the labels for each frame [Object detection]
3. Among all of these frames we select the most representative one through a clustering algorithm [Best frame selection]
4. We use a vision model, called moondream2, to get the frame description with a proper prompt [Frame description]
5. We pass the description to the model that refines the prompt for the audio generation model [Prompt enhancer]
6. We generate the audio from the prompt [Audio generation]
7. We mix the audio with the video [Reconstructor]

There is an additional feature that makes even possible to generate sounds from the video itself. Obviously this is a very hard task to do in order to make it realistic, but that was not the main goal of the project. It was just a nice feature to have and to show the potential of the application.

All of this is built on top of Gradio, a Python library that allows us to create interfaces for our models. This way, we can easily ship the application on a web interface ready to be used by anyone.
All the modules are working standalone, so anynone can look the code and built the proper pipeline for their own use case. 
For our case, we had 2 possible workflows:

1. Video -> Audio
2. Picture -> Audio

So now, let's see the actual results of the application!

*Examples in the video*

Final part:

Of course this is just a very simple implementation of what could be done. We could improve the model, the interface, the pipeline, and so on. The code is available on our GitHub repository, so feel free to check it and if you want to use or to improve it, feel free to do so! 