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

# get duration of intro and add it to total_duration
intro_file = "0-intro-withMusic.mp3"
intro_tag = TinyTag.get(os.path.join(audio_folder_path, intro_file))
total_duration += intro_tag.duration

# Add intro chapter
chapters.append(
    {
        "startTime": 0,
        "title": "Intro",
        "url": None,
    }
)

# create a list of mp3 files, sorted in numerical order (excluding intro and outro)
mp3_files = sorted(
    [
        f
        for f in os.listdir(audio_folder_path)
        if f.endswith(".mp3") and f != intro_file and not f.endswith("_outro.mp3")
    ],
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
            "title": detail.get(
                "title", f"Chapter {i+1}"
            ),  # Changed from "Chapter {i}" to "Chapter {i+1}" to account for the intro chapter
            "url": detail.get("link", None),
        }
    )

    # increase the total duration
    total_duration += duration

# get duration of outro and add it to total_duration
outro_file = next(
    (f for f in os.listdir(audio_folder_path) if f.endswith("_outro.mp3")), None
)
if outro_file:
    outro_tag = TinyTag.get(os.path.join(audio_folder_path, outro_file))
    total_duration += outro_tag.duration

    # Add outro chapter
    chapters.append(
        {
            "startTime": round(total_duration),
            "title": "Outro",
            "url": None,
        }
    )

# save the chapters to a json file
with open(os.path.join(folder_path, "chapters.json"), "w") as f:
    json.dump({"version": "1.2.0", "chapters": chapters}, f)
