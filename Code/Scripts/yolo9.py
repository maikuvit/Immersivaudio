from ultralytics import YOLO
import sys

model = YOLO("yolov9e.pt", verbose = False)  # load an official model

def get_yolo_labels(input_json):

    res = model(input_json["frame_extraction"]["output_path"], conf=0.25)

    result = []
    total_keywords = set()
    for ix, r in enumerate(res):
        els = set()
        # If there are no boxes, skip
        try:
            # use r.boxes and not r[0].boxes to get all boxes
            for c in r.boxes.cls:
                els.add(model.names[int(c)])
                total_keywords.add(model.names[int(c)])
        except:
            pass
        
        result.append({"frame": ix + 1, "labels": list(els)})

    json_result = {"total_keywords": list(total_keywords), "frames": result}
    input_json.update({"object_detection": json_result})
    return input_json

if "__main__" == __name__:
    print(get_yolo_labels(" ".join(sys.argv[1:])))

