from ultralytics import YOLO
import os
import json
import json

model = YOLO("yolov8n.pt")  # load an official model

def get_yolo_labels(input_json):

    images = os.listdir(input_json["output_path"])
    # sort images by number
    images.sort(key=lambda x: int(x.split(".")[0]))

    res = model(input_json["output_path"], conf=0.25)

    result = []
    for ix, r in enumerate(res):
        els = set()
        # If there are no boxes, skip
        try:
            # use r.boxes and not r[0].boxes to get all boxes
            for c in r.boxes.cls:
                els.add(model.names[int(c)])
        except:
            pass
        
        result.append({"frame": ix, "labels": list(els)})

    json_result = json.dumps(result)

    return json_result