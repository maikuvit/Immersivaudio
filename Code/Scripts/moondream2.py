from transformers import AutoModelForCausalLM, AutoTokenizer
from PIL import Image
import torch
import json
import sys
import gc 

def frame_description(input_json):
    
    best_frame = input_json["frame_selection"]["best_frame"]

    model_id = "vikhyatk/moondream2"
    revision = "2024-04-02"

    model = AutoModelForCausalLM.from_pretrained(
        model_id, trust_remote_code=True, revision=revision
    )
    # model = "daje"

    tokenizer = AutoTokenizer.from_pretrained(model_id, revision=revision)

    image = Image.open(best_frame)

    if torch.cuda.is_available():
        model.to('cuda')
    # response = "What a nice dog! (this text is mocked, but dogs are always amazing) " #mock because it can not be run locally 
    enc_image = model.encode_image(image)
    response = model.answer_question(enc_image, "Describe shortly the image and give it a mood that describes it.", tokenizer)
    out = {
            "description" : response
        }
    
    
    print("Unloading Moondream2 model...")
    del model
    gc.collect()
    torch.cuda.empty_cache()

    input_json.update({"frame_description": out})
    return input_json


if "__main__" == __name__:
    print(frame_description(" ".join(sys.argv[1:])))

'''
'{"video_id" : "gatto", "best_frame" : "Code/Scripts/output/cat/10.jpg" }'
'''