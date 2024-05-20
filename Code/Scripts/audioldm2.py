import scipy
import torch
from diffusers import AudioLDM2Pipeline
from diffusers import DPMSolverMultistepScheduler
import json
import os

repo_id = "cvssp/audioldm2"
# repo_id = "cvssp/audioldm2-large"

def audo_generate(input_json):
    input_json = json.loads(input_json)
    
    """
    Tips for the prompting: 
    1. Not too long
    2. Include the keywords that you want to be in the audio
    3. If you want musicm add "music" or "song" in the prompt, in the end is better
    4. If you want high quality audio, add "high quality" in the prompt
    """

    prompt = "Beautiful song inspired by " + input_json["description"] + ", high quality"
    negative_prompt = "Low quality, average quality, bad quality, poor quality"
    video_id = input_json["video_id"]

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
        audio_length_in_s=10.0,
        num_inference_steps=100,
        guidance_scale=3.5
    )

    # save the audio
    audio = audio.audios[0]


    dir_path = os.path.dirname(os.path.realpath(__file__))
    audio_path = os.path.join(dir_path, "output/audio")
    os.makedirs(audio_path, exist_ok=True)
    audio_path = os.path.join(audio_path, f"{video_id}.wav")
    scipy.io.wavfile.write(audio_path, 16000, audio)

    return f"Audio generate in {audio_path}" 
    
if __name__ == "__main__":
  input_json = {
      "description": "The sound depicts the ambient noises of a quiet room. A gentle rustling of fabric can be heard as a young man with long, dark hair wearing glasses adjusts his blue jacket. The soft click of a camera shutter echoes as he takes a selfie. In the background, the faint creak of a chair and the subtle hum of a quiet space can be heard.",
      "video_id": "/content/videos/cat.mp4" 
  }
  print(audo_generate(json.dumps(input_json)))
    