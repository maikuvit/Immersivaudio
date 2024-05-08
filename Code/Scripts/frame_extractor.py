import math
import os
import subprocess
import sys
import cv2 as cv


def extract_frames(video_path, output_path, fps):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    video_name = os.path.basename(video_path)
    output_folder = os.path.join(output_path, video_name)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    command = f"ffmpeg -i {video_path} -vf fps={fps} {output_folder}/%d.jpg -hide_banner -loglevel error"
    subprocess.call(command, shell=True)

def fps_count(seconds, factor):
    return math.floor(math.log(seconds,10) * factor)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python frame_extractor.py <video_path> <output_path> <fps factor>")
        sys.exit(1)
    video_path = sys.argv[1]
    output_path = sys.argv[2]
    factor = (int) (sys.argv[3])

    video = cv.VideoCapture(video_path)

    fps = video.get(cv.CAP_PROP_FPS)
    frame_count = video.get(cv.CAP_PROP_FRAME_COUNT)

    sec = (int) (frame_count / fps) 

    frames = fps_count( sec, factor)
    fps = math.floor(frames / sec * 100) / 100 # floor to two decimal places

    print(f"Total extracted frames: {frames}\nSeconds video duration: {sec}\nFPS: {fps}")    
    extract_frames(video_path, output_path, fps)
    print("Frames extracted successfully")



