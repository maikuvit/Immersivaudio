class VideoJson:

    def __init__(self, output_path, frame_count, video_id):
        self.output_path = output_path
        self.frame_count = frame_count
        self.video_id = video_id

    def __str__(self):
        return f"VideoJson(output_path={self.output_path}, frame_count={self.frame_count}, video_id={self.video_id})"
    
