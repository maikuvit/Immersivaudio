import scipy
import torch
from diffusers import AudioLDM2Pipeline
from diffusers import DPMSolverMultistepScheduler
import json
import os

repo_id = "cvssp/audioldm2"
# repo_id = "cvssp/audioldm2-large"
# repo_id = "cvssp/audioldm2-music"


def audio_generate(input_json):

    prompt = input_json["prompt_combiner"]["prompt"]
    video_name = input_json["video_input"]["video_name"]

    negative_prompt = "Low quality, average quality, bad quality, poor quality"

    pipe = AudioLDM2Pipeline.from_pretrained(repo_id, torch_dtype=torch.float16)
    if torch.cuda.is_available():
        pipe = pipe.to("cuda")

        # set the seed for generator
        pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
        pipe.enable_model_cpu_offload()

    # run the generation
    print(f"Generating with prompt: \n {prompt} ")

    audio = pipe(
        prompt,
        negative_prompt=negative_prompt,
        num_waveforms_per_prompt=4,
        audio_length_in_s=int(input_json["video_input"]["video_duration"]),
        num_inference_steps=75,
        guidance_scale=3.5,
    )

    # save the audio
    audio = audio.audios[0]
    audio_path = input_json["video_input"]["output_path"]
    os.makedirs(audio_path, exist_ok=True)
    audio_path = os.path.join(audio_path, f"{video_name}.wav")
    scipy.io.wavfile.write(audio_path, 16000, audio)
    print("Audio generated in: ", audio_path)

    if input_json["options"]["generate_sounds"]:
        #  generate sounds
        prompt = input_json["prompt_combiner"]["sound_prompt"]
        print(f"Generating with prompt: \n {prompt} ")
        audio = pipe(
            prompt,
            negative_prompt=negative_prompt,
            num_waveforms_per_prompt=4,
            audio_length_in_s=int(input_json["video_input"]["video_duration"]),
            num_inference_steps=75,
            guidance_scale=3.5,
        )

        # save the audio
        audio = audio.audios[0]
        sound_path = input_json["video_input"]["output_path"]
        os.makedirs(sound_path, exist_ok=True)
        sound_path = os.path.join(sound_path, f"{video_name}_sounds.wav")
        scipy.io.wavfile.write(sound_path, 16000, audio)
        print("Audio generated in: ", sound_path)

    out = {"audio_generation": {"path": audio_path}}

    if input_json["options"]["generate_sounds"]:
        out.update({"sound_generation": {"path": sound_path}})

    input_json.update(out)
    return input_json


if __name__ == "__main__":

    input_json = {
        "prompt_combiner": {
            "prompt": "The image portrays tranquility in nature through its peaceful setting, featuring a calm canine companion amidst verdant foliage.",
        },
        "video_input": {"video_name": "/content/videos/test.mp4"},
    }

    print(audio_generate(json.dumps(input_json)))
