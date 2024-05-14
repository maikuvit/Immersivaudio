# Example of usage
import os
import json
from moondream2 import frame_description
from frame_extractor import frame_extraction
from best_frame_selection import get_best_frame
from yolo8 import get_yolo_labels

# 1. Get the video
dir_path = os.path.dirname(os.path.realpath(__file__))
video_path = os.path.join(dir_path, "../videos/cat.mp4")

def main(video_path):

    history = []
    # 2. Extract frames
    input_json = {
        "video_path": video_path,
        "output_path": os.path.join(dir_path, "output"),
        "factor": 10
    }
    input_json = json.dumps(input_json)
    extraction = frame_extraction(input_json, verbose=False)
    print(f"[OUTPUT] {json.loads(extraction)['frame_count']}")

    history.append(f"Extracted {json.loads(extraction)['frame_count']} frames.")

    # 3. Get frames labels using YOLO
    labels = get_yolo_labels(extraction)

    print("Labels for the frames:")
    history.append("Labels for the frames:")
    labels = json.loads(labels)
    for l in labels:
        print(f"[OUTPUT] {l}")
        history.append(l)

    # 4. Get the best frame
    best_frame = get_best_frame(extraction)

    print(f"[OUTPUT] {best_frame}")
    history.append(f"best frame at {best_frame}")

    # 5. Get the description of the best frame
    description = frame_description(best_frame)
    print(f"[OUTPUT] {description}")
    history.append(f"Best frame description: {description}")

    return [history[0], json.loads(best_frame)["best_frame"], json.loads(description)["description"]]

if __name__ == "__main__":
    main(video_path)