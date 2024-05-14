# Immersivaudio

Learning-Based Multimedia Processing incredible project I mean we are amazing sium 

## Project Overview

This project is focused on video processing and analysis. It uses a combination of frame extraction, object detection, and natural language processing to analyze and describe the content of videos.

### Scripts Folder

The Scripts folder contains the main Python scripts that perform the video processing tasks. Here's a brief overview of each script:

`best_frame_selection.py`: This script contains the get_best_frame function which selects the best frame from a video based on certain criteria.

`frame_extractor.py`: This script is responsible for extracting frames from a video. It uses the output_path variable to determine where to save the extracted frames.

`main.py`: This is the main script that ties everything together. It uses the functions from the other scripts to extract frames from a video, get labels for the frames using YOLO, select the best frame, and generate a description of the best frame.

`moondream2.py`: This script contains the frame_description function which generates a description of a given frame.

`yolo8.py`: This script uses the YOLO (You Only Look Once) real-time object detection system to get labels for the frames extracted from a video.

### Notebooks

The Code folder also contains several Jupyter notebooks (.ipynb files) that demonstrate the usage of the scripts and the overall video processing workflow. The notebooks vit_gpt2.ipynb and vit-gpt2.ipynb in particular, show the output of the GPT-2 model generating descriptions of video frames.

### Videos

The videos folder in the Code directory contains the video files that are processed by the scripts.

### Results

The results folder contains the output of the video processing tasks, including a CSV and JSON file with the results.

### Dependencies
This project uses Python and requires several libraries, including YOLO for object detection and GPT-2 for text generation.