import json

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import os
# Load the data from the JSON file
# get current directory


with open("Code/Presentation/data.json", "r") as f:
    data = json.load(f)
    
lengths = ['1m', '45sec', '30sec', '15sec', '5sec']
time_keys = ['extraction_time', 'labels_time', 'best_frame_time', 'description_time', 'prompt_time', 'audio_time', 'reconstruct_time', 'total_time']


# For each time key
for key in time_keys:
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_title(f'Metric: {key}')
    ax.set_xlabel('Video Length')
    ax.set_ylabel('Time (Seconds)')

    times = []
    for length in lengths:
        video_times = []
        for video in range(1, 6):
            video_times.append(data[f'Video {video} - {length}'][key])
        times.append(sum(video_times) / len(video_times))  # Calcola la media

    sns.barplot(x=lengths, y=times, palette=sns.color_palette("dark:#9a92e9_r", n_colors=5), hue=lengths)
    ax.set_xticks(lengths)

    plt.tight_layout()
    plt.savefig(f'Code/Presentation/graphs/{key}.png')
    plt.close()

