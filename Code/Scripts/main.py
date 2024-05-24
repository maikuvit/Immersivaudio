# Example of usage
import hashlib
import os
from video_reconstructor import reconstruct_output
from prompt_combiner import recombine_prompt
from moondream2 import frame_description
from frame_extractor import frame_extraction
from best_frame_selection import get_best_frame
from yolo9 import get_yolo_labels
from audioldm2 import audio_generate

# 1. Get the video
dir_path = os.path.dirname(os.path.realpath(__file__))
video_path = os.path.join(dir_path, "../videos/cat.mp4")

BUF_SIZE = 65536  # lets read stuff in 64kb chunks!

image_formats = ["jpg", "jpeg", "png", "bmp", "gif", "tiff", "webp"]


# generate a video token ...
def filehash(file):

    md5 = hashlib.md5()
    with open(file, "rb") as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            md5.update(data)

    md5.update("someRandomTextToAvoidAttacks".encode())

    return md5.hexdigest()


def main(
    video_path, generate_sounds: bool, seconds=10, music_volume=0.5, sound_volume=0.0
):
    if video_path.split(".")[-1] in image_formats:
        return image_pipeline(
            video_path, generate_sounds, seconds, music_volume, sound_volume
        )
    else:
        return video_pipeline(video_path, generate_sounds, music_volume, sound_volume)


def image_pipeline(
    image_path, generate_sounds: bool, seconds=5, music_volume=0.5, sound_volume=0.0
):
    os.rename(image_path, image_path.replace(" ", "_"))
    image_path = image_path.replace(" ", "_")
    token = filehash(image_path)

    # 1. Input json construction
    input_json = {
        "token": token,
        "video_name": os.path.basename(image_path),
        "video_path": image_path,
        "output_path": os.path.join(dir_path, "output", token),
        "file_format": image_path.split(".")[-1],
    }

    options = {
        "generate_sounds": generate_sounds,
        "music_volume": music_volume,
        "sound_volume": sound_volume,
    }

    input_json = {"video_input": input_json}
    input_json.update({"options": options})

    # 3. Mocked frame extraction json
    input_json["video_input"]["video_duration"] = seconds
    frame_extraction = {
        "frame_extraction": {
            "output_path": os.path.join(
                input_json["video_input"]["output_path"], "1.jpg"
            ),
            "frame_count": 1,
        }
    }
    input_json.update(frame_extraction)

    # If not exists, create the output directory
    if not os.path.exists(input_json["video_input"]["output_path"]):
        os.makedirs(input_json["video_input"]["output_path"])
    # copy the image to the output directory
    os.system(
        f"cp {input_json['video_input']['video_path']} {input_json['video_input']['output_path']}/1.jpg"
    )

    # 4. YOLO labels
    labels = get_yolo_labels(input_json)

    # 5. Mock best frame
    frame_selection = {
        "best_frame": os.path.join(input_json["video_input"]["output_path"], "1.jpg"),
        "best_frame_idx": 0,
    }

    input_json.update({"frame_selection": frame_selection})

    # 6. Description
    description = frame_description(input_json)

    # 7. Prompt
    prompt = recombine_prompt(description, labels)

    # 8. Audio
    audio = audio_generate(prompt)

    # 9. Reconstruct output
    final = reconstruct_output(audio)

    return [
        final["video_reconstruction"]["output_path"],
        final["audio_generation"]["path"],
        final["prompt_combiner"]["prompt"],
        final,
    ]


def video_pipeline(video_path, generate_sounds: bool, music_volume=0.5, sound_volume=0.0):
    print(video_path)

    os.rename(video_path, video_path.replace(" ", "_"))
    video_path = video_path.replace(" ", "_")
    token = filehash(video_path)
    # 2. Extract frames
    input_json = {
        "token": token,
        "video_name": os.path.basename(video_path),
        "video_path": video_path,
        "output_path": os.path.join(dir_path, "output", token),
        "factor": 10,
        "file_format": video_path.split(".")[-1],
    }

    options = {
        # "file_format": "mp4",
        # "keep_audio": True,
        # "original_volume" : 80,
        "generate_sounds": generate_sounds,
        "music_volume": music_volume,
        "sound_volume": sound_volume,
    }

    input_json = {"video_input": input_json}
    input_json.update({"options": options})
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

    return [
        final["video_reconstruction"]["output_path"],
        final["audio_generation"]["path"],
        final["prompt_combiner"]["prompt"],
        final,
        # Knowing that "final" is a json, pretty print it
    ]


if __name__ == "__main__":
    main(video_path)
