from ultralytics import YOLO
import os
import json
from utils import VideoJson
import json

model = YOLO("yolov8n.pt")  # load an official model

def get_yolo_labels(input_json):

    images = os.listdir(input_json["output_path"])
    # sort images by number
    images.sort(key=lambda x: int(x.split(".")[0]))

    res = model(input_json["output_path"])

    result = []
    for ix, r in enumerate(res):
        els = set()
        for c in r[0].boxes.cls:
            els.add(model.names[int(c)])
        result.append({"frame": ix, "labels": list(els)})

    json_result = json.dumps(result)

    return json_result