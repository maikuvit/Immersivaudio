import scipy
import torch
from diffusers import AudioLDM2Pipeline
import json
import os
from diffusers import DPMSolverMultistepScheduler

repo_id = "cvssp/audioldm2"


def audo_generate(input_json):
    input_json = json.loads(input_json)
    prompt = input_json["description"]
    negative_prompt = "Low quality, average quality, bad quality, poor quality, terrible quality, bad audio"
    video_id = input_json["video_id"]

    pipe = AudioLDM2Pipeline.from_pretrained(repo_id, torch_dtype=torch.float16)
    if torch.cuda.is_available():
        pipe = pipe.to("cuda")

        # set the seed for generator
        generator = torch.Generator("cuda").manual_seed(0)
        pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
        pipe.enable_model_cpu_offload()

    # run the generation
    audio = pipe(
        prompt,
        negative_prompt=negative_prompt,
        num_waveforms_per_prompt=1,
        audio_length_in_s=20,
        num_inference_steps=50,
        generator=generator.manual_seed(0),
    ).audios[0]

    dir_path = os.path.dirname(os.path.realpath(__file__))
    audio_path = os.path.join(dir_path, "output/audio")
    scipy.io.wavfile.write(f"{audio_path}/{video_id}.wav", rate=16000, data=audio[0])

    return f"{audio_path}/{video_id}.wav"
