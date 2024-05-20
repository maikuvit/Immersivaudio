
import subprocess
import os


def reconstruct_output(input_json):

    video_path = input_json["video_input"]["video_path"]
    audio_path = input_json["audio_generation"]["path"]

    output_path = input_json["video_input"]["output_path"]

    # constructing the output filename 
    output_filename = input_json["video_input"]["video_name"] + "_enhanced.mp4"

    # Remove audio from original video with bash ffmpeg
    temp_video_path = os.path.join(output_path, "temp_video.mp4")
    ffmpeg_remove_audio_cmd = f"ffmpeg -i {video_path} -c copy -an {temp_video_path}"
    subprocess.call(ffmpeg_remove_audio_cmd, shell=True)

    # Run ffmpeg on bash to join video and audio
    ffmpeg_cmd = f"ffmpeg -i {temp_video_path} -i {audio_path} -c:v copy -c:a aac -strict experimental {output_filename}"
    subprocess.call(ffmpeg_cmd, shell=True)

    os.remove(temp_video_path)

    input_json.update({"video_reconstruction": {"output_path": output_path}})
    return input_json