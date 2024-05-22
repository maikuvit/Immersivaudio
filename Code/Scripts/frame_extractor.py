import math
import os
import subprocess
import sys
import cv2 as cv
import json


import os
import subprocess

def extract_frames(video_path, output_path, fps):
    """
    Extract frames from a video file and save them as individual images.

    Args:
        video_path (str): The path to the video file.
        output_path (str): The path to the output folder where the frames will be saved.
        fps (int): The desired frames per second for the extracted frames.

    Returns:
        None
    """
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    video_name = os.path.basename(video_path)

    # remove the file extension
    video_name = os.path.splitext(video_name)[0]
    output_folder = os.path.join(output_path, video_name)
    print(output_folder)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    print(f"Extracting frames to {output_folder}")

#    # Handle the fact that the directory may contain whitespaces
#    video_path = f'"{video_path}"'
#    output_folder = f'"{output_folder}"'

    command = f"ffmpeg -i {video_path} -vf fps={fps} {output_folder}/%d.jpg"
    subprocess.call(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def fps_count(seconds, factor):
    """
    Calculate the number of frames per second based on the number of seconds and a factor.

    Args:
        seconds (int): The number of seconds in the video.
        factor (float): The factor to use in the calculation.
    """
    return math.floor(math.log(seconds, 10) * factor)



# json for the input
def frame_extraction(input_json, verbose=False):
    """
    Extract frames from a video file and save them as individual images.
    
    Args:
        video_path (str): The path to the video file.
        output_path (str): The path to the output folder where the frames will be saved.
        factor (float): The factor to use in the calculation of the frames per second.
        verbose (bool): Whether to print additional information.
    """
    input_json = json.loads(input_json)

    video_path = input_json["video_input"]["video_path"]
    output_path = input_json["video_input"]["output_path"]
    factor = (int) (input_json["video_input"]["factor"])
    # input_json = {"video_input" : input_json}
    
    if not os.path.exists(video_path):
        print(f"Video path: {video_path}")
        print("Video file does not exist")
        sys.exit(1)

    video = cv.VideoCapture(video_path)

    fps = video.get(cv.CAP_PROP_FPS)
    frame_count = video.get(cv.CAP_PROP_FRAME_COUNT)

    sec = (int)(frame_count / fps)

    frames = fps_count(sec, factor)
    fps = math.floor(frames / sec * 100) / 100  # floor to two decimal places

    if verbose:
        print(
            f"Total extracted frames: {frames}\nSeconds video duration: {sec}\nFPS: {fps}"
        )
    extract_frames(video_path, output_path, fps)
    if verbose:
        print("Frames extracted successfully")

    input_json["video_input"]["video_duration"] = sec

    frame_extraction = {
         'frame_extraction':
            {
            'output_path': os.path.join(output_path, os.path.splitext(os.path.basename(video_path))[0]),
            'frame_count': frames,
        }
    }

    input_json.update(frame_extraction)
    return input_json

if "__main__" == __name__:
    frame_extraction(" ".join(sys.argv[1:]))

'''
{"video_path" : "../videos/cat.mp4", "output_path" : "cat3", "factor" : "10"}
'''