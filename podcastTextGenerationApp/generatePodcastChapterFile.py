#!/usr/bin/env python3

import os
import sys
import json
import re
from tinytag import TinyTag


def extract_number(filename):
    match = re.match(r"(\d+)", filename)
    if match:
        return int(match.group(1))
    return 0  # Default to 0 if no number is found


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

# create a list of mp3 files, sorted by the leading number
mp3_files = sorted(
    [f for f in os.listdir(audio_folder_path) if f.endswith(".mp3")], key=extract_number
)

# Add intro chapter at 0:00
chapters.append(
    {
        "startTime": 0,
        "title": "Intro",
        "url": None,
    }
)

for i, mp3_file in enumerate(mp3_files):
    # get the duration of the current mp3 file
    tag = TinyTag.get(os.path.join(audio_folder_path, mp3_file))
    duration = tag.duration

    # get the corresponding podcast detail (if available)
    file_number = extract_number(mp3_file)
    detail = next(
        (item for item in podcast_details if item["itemOrder"] == file_number - 1), {}
    )

    # add a chapter (skip if it's the intro file)
    if "_intro" not in mp3_file and "-intro" not in mp3_file:
        chapters.append(
            {
                "startTime": round(total_duration),
                "title": detail.get(
                    "title", f"Chapter {i+1}"
                ),  # +1 to account for intro
                "url": detail.get("link", None),
            }
        )

    # increase the total duration
    total_duration += duration

# save the chapters to a json file
with open(os.path.join(folder_path, "chapters.json"), "w") as f:
    json.dump({"version": "1.2.0", "chapters": chapters}, f)

print("Chapter file generated successfully.")
