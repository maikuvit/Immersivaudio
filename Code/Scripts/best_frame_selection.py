import sys
import torch
import json
from PIL import Image
from torchvision import transforms
import numpy as np
from sklearn_extra.cluster import KMedoids


# model loading ...
model = torch.hub.load('pytorch/vision:v0.10.0', 'resnet18', pretrained=True)
if torch.cuda.is_available():
    model = model.to('cuda')
model.eval()

def get_best_frame(input_json):

    inputPath = input_json["frame_extraction"]["output_path"]
    frames_number = input_json["frame_extraction"]["frame_count"]


    # Load the images
    images = {}
    for i in range(1,frames_number + 1):
        img_name = inputPath + "/" + str(i) + ".jpg" 
        img = Image.open(img_name)
        images[img_name] = (img)


    activation = None

    def hook(model, input, output):
        nonlocal activation
        activation = output


    preprocess = transforms.Compose([
        transforms.Resize(512),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    latent = {}
    for i in images:
        input_tensor = preprocess(images[i])   
        input_batch = input_tensor.unsqueeze(0)

        # move the input and model to GPU for speed if available
        if torch.cuda.is_available():
            input_batch = input_batch.to('cuda')

        model.layer3[1].conv2.register_forward_hook(hook)

        with torch.no_grad():
            model(input_batch)
        latent[i] = activation[0]


    #  initial shape 512 x 16 x 29, need to reshape everything to 1 x (512*16*29) then stack to 
    flattened_arrays = [arr.cpu().flatten() for arr in latent.values()]

    flattened_data = np.vstack(flattened_arrays)

    med_model = KMedoids(n_clusters=1, random_state=0)

    med_model.fit(flattened_data)

    # Trovare il medoide
    medoid_index = med_model.medoid_indices_[0]

    frame_selection = {
        "best_frame" : list(images.keys())[medoid_index],
        "best_frame_idx" : medoid_index
    }

    input_json.update({"frame_selection": frame_selection})

    return input_json

if "__main__" == __name__:
    print(get_best_frame(" ".join(sys.argv[1:])))

'''
{"output_path": "Code/Scripts/cat3","frame_count": "14"}
'''