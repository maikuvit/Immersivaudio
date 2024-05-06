import os
import subprocess
import sys

def extract_frames(video_path, output_path, fps):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    video_name = os.path.basename(video_path)
    output_folder = os.path.join(output_path, video_name)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    command = f"ffmpeg -i {video_path} -vf fps={fps} {output_folder}/%d.jpg"
    subprocess.call(command, shell=True)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python frame_extractor.py <video_path> <output_path> <fps>")
        sys.exit(1)
    video_path = sys.argv[1]
    output_path = sys.argv[2]
    fps = sys.argv[3]
    extract_frames(video_path, output_path, fps)
    print("Frames extracted successfully")
