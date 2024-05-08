# Example of usage
import os
import json
from frame_extractor import frame_extraction
from yolo8 import get_yolo_labels

# 1. Get the video
dir_path = os.path.dirname(os.path.realpath(__file__))
video_path = os.path.join(dir_path, "../videos/cat.mp4")

# 2. Extract frames
input_json = {
    "video_path": video_path,
    "output_path": os.path.join(dir_path, "output"),
    "factor": 10

}
extraction = frame_extraction(input_json, verbose=False)
print(f"The extraction is:")
print(json.dumps(extraction, indent=4))

# 3. Get frames labels using YOLO
labels = get_yolo_labels(extraction)

print(f"Labels for the frames:")
for l in json.loads(labels):
    print(l)