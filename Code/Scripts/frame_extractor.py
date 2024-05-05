# Using ffmpeg
# Extract 2 frames each seconds of a video
# save the frames in a folder with the same name as the video and an id

import os
import subprocess
import sys

def extract_frames(video_path, output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    video_name = os.path.basename(video_path)
    output_folder = os.path.join(output_path, video_name)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    command = "ffmpeg -i " + video_path + " -vf fps=2 " + output_folder + "/%d.jpg"
    subprocess.call(command, shell=True)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python frame_extractor.py <video_path> <output_path>")
        sys.exit(1)
    video_path = sys.argv[1]
    output_path = sys.argv[2]
    extract_frames(video_path, output_path)
    print("Frames extracted successfully")