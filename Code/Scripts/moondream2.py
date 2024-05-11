from transformers import AutoModelForCausalLM, AutoTokenizer
from PIL import Image
import torch
import json
import sys

def frame_description(input_json):

    input_json = json.loads(input_json)
    
    best_frame = input_json["best_frame"]
    video_id = input_json["video_id"]

    model_id = "vikhyatk/moondream2"
    revision = "2024-04-02"

    model = AutoModelForCausalLM.from_pretrained(
        model_id, trust_remote_code=True, revision=revision
    )
    #model = "daje"

    tokenizer = AutoTokenizer.from_pretrained(model_id, revision=revision)

    image = Image.open(best_frame)

    if torch.cuda.is_available():
        model.to('cuda')
    #response = "daje Roma daje " #mock because it can not be run locally 
    enc_image = model.encode_image(image)
    response = model.answer_question(enc_image, "Describe this image considering it will be used as input to a sound generation model.", tokenizer)
    out = json.dumps(
        {
            "video_id" : video_id,
            "frame" : best_frame,
            "description" : response})
    
    return out


if "__main__" == __name__:
    print(frame_description(" ".join(sys.argv[1:])))

'''
'{"video_id" : "gatto", "best_frame" : "Code/Scripts/output/cat/10.jpg" }'
'''