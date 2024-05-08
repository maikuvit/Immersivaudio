from ultralytics import YOLO
import os
import json

model = YOLO('yolov8n.pt')  # load an official model


filename = 'room.mp4'


# read images from images folder
images = os.listdir(f'Scripts/{filename.split(".")[0]}/{filename}')

# sort images by number
# ['1.jpg', '10.jpg', '11.jpg', '2.jpg', '3.jpg', '4.jpg', '5.jpg', '6.jpg', '7.jpg', '8.jpg', '9.jpg']

images.sort(key=lambda x: int(x.split('.')[0]))


res = []

for image in images:
    with open(f'results/results.json', 'w') as f:
        f.write('[')
        for ix, r in enumerate(res):
            els = set()
            for c in r[0].boxes.cls:
                els.add(model.names[int(c)])
            f.write(json.dumps({'frame': ix, 'labels': list(els)}))
            if ix != len(res) - 1:
                f.write(',\n')
        f.write(']')

print(res)


with open(f'results/results.json', 'w') as f:
    f.write('[')
    for ix, r in enumerate(res):
        els = set()
        for c in r[0].boxes.cls:
            els.add(model.names[int(c)])
        f.write(json.dumps({'frame': ix, 'labels': list(els)}))
        if ix != len(res) - 1:
            f.write(',\n')
    f.write(']')