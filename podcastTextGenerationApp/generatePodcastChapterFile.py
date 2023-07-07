import os
import sys
import json
from tinytag import TinyTag

# check if the folder_path argument is provided
if len(sys.argv) < 2:
    print(
        "Please provide the path to the folder containing your mp3 files as a command line argument."
    )
    sys.exit(1)

# the path to the folder containing your mp3 files
folder_path = sys.argv[1]
audio_folder_path = os.path.join(folder_path, "audio")

# load the podcast details
with open(os.path.join(folder_path, "podcastDetails.json"), "r") as f:
    podcast_details = json.load(f)

# list to store the chapters
chapters = []

# counter for total duration
total_duration = 0

# create a list of mp3 files, sorted in numerical order
mp3_files = sorted(
    [f for f in os.listdir(audio_folder_path) if f.endswith(".mp3")],
    key=lambda x: os.path.splitext(x)[0],
)

for i, mp3_file in enumerate(mp3_files):
    # get the duration of the current mp3 file
    tag = TinyTag.get(os.path.join(audio_folder_path, mp3_file))
    duration = tag.duration

    # get the corresponding podcast detail (if available)
    detail = podcast_details[i] if i < len(podcast_details) else {}

    # add a chapter
    chapters.append(
        {
            "startTime": round(total_duration),
            "title": detail.get("title", f"Chapter {i}"),
            "url": detail.get("link", None),
        }
    )

    # increase the total duration
    total_duration += duration

# save the chapters to a json file
with open(os.path.join(folder_path, "chapters.json"), "w") as f:
    json.dump({"version": "1.2.0", "chapters": chapters}, f)
