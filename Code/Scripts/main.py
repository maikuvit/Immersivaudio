# Example of usage
import hashlib
import os
import json
from video_reconstructor import reconstruct_output
from prompt_combiner import recombine_prompt
from moondream2 import frame_description
from frame_extractor import frame_extraction
from best_frame_selection import get_best_frame
from yolo8 import get_yolo_labels
from audioldm2 import audio_generate

# 1. Get the video
dir_path = os.path.dirname(os.path.realpath(__file__))
video_path = os.path.join(dir_path, "../videos/cat.mp4")

BUF_SIZE = 65536  # lets read stuff in 64kb chunks!


# generate a video token ...
def filehash(file):

    md5 = hashlib.md5()
    with open(file, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            md5.update(data)

    
    md5.update("someRandomTextToAvoidAttacks".encode())

    return md5.hexdigest()


def main(video_path):
    video_path = video_path.replace(" ", "_")
    token = filehash(video_path)
    # 2. Extract frames
    input_json = {
        "token": token,
        "video_name": os.path.basename(video_path),
        "video_path": video_path,
        "output_path": os.path.join(dir_path, "output", token),
        "factor": 10
    }
    input_json = json.dumps(input_json)
    extraction = frame_extraction(input_json, verbose=False)

    # 3. Get frames labels using YOLO
    labels = get_yolo_labels(extraction)

    # 4. Get the best frame
    best_frame = get_best_frame(extraction)

    # 5. Get the description of the best frame
    description = frame_description(best_frame)

    # 6. Combine the outputs to generate the prompt
    prompt = recombine_prompt(description, labels)

    # 7. Generate audio
    audio = audio_generate(prompt)
    

    # 8. Reconstruct the video
    final = reconstruct_output(audio)

    return [final["video_reconstruction"]["output_path"],
            final["audio_generation"]["path"],
            final["prompt_combiner"]["prompt"],
            final
            ]

if __name__ == "__main__":
    main(video_path)