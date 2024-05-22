
import subprocess
import os


def reconstruct_output(input_json):

    video_path = input_json["video_input"]["video_path"]
    audio_path = input_json["audio_generation"]["path"]

    if input_json['options']['generate_sounds']:
        sound_path = input_json["sound_generation"]["path"]

    output_path = input_json["video_input"]["output_path"]

    # Run ffmpeg command to join video and audio
    output_filename = input_json["video_input"]["video_name"] + "_enhanced.mp4"
    output_path = os.path.join(os.path.dirname(output_path), output_filename)

    # Remove audio from original video
    temp_video_path = os.path.join(os.path.dirname(output_path), "temp_video.mp4")
    ffmpeg_remove_audio_cmd = f"ffmpeg -i {video_path} -c copy -an {temp_video_path}"
    subprocess.call(ffmpeg_remove_audio_cmd, shell=True)

    # Join video and audio
    ffmpeg_cmd = f"ffmpeg -y -i {temp_video_path} -i {audio_path} -c:v copy -c:a aac -strict experimental {output_path}"
    subprocess.call(ffmpeg_cmd, shell=True)

    # Remove temp video
    os.remove(temp_video_path)

    if input_json['options']['generate_sounds']:
        # use sound_path to add sounds to the previous output
        temp_output_path = os.path.join(os.path.dirname(output_path), "temp_output.mp4")
        ffmpeg_add_audio_cmd = f"ffmpeg -y -i {output_path} -i {sound_path} -filter_complex '[0:a]volume=0.95[a];[1:a]volume=1.0[b];[a][b]amix=inputs=2:duration=first:dropout_transition=1' {temp_output_path}"
        subprocess.call(ffmpeg_add_audio_cmd, shell=True)
        os.remove(output_path)
        os.rename(temp_output_path, output_path)

    input_json.update({"video_reconstruction": {"output_path": output_path}})
    return input_json