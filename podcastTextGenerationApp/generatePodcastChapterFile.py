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


def find_matching_story_file(mp3_file, story_files):
    mp3_name = os.path.splitext(mp3_file)[0]
    for story_file in story_files:
        story_name = os.path.splitext(story_file)[0]
        if mp3_name.endswith(story_name) or story_name in mp3_name:
            return story_file
    return None


# check if the folder_path argument is provided
if len(sys.argv) < 2:
    print(
        "Please provide the path to the folder containing your mp3 files as a command line argument."
    )
    sys.exit(1)

# the path to the folder containing your mp3 files
folder_path = sys.argv[1]
audio_folder_path = os.path.join(folder_path, "audio")
stories_folder_path = os.path.join(folder_path, "stories")

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

# Process each MP3 file
for mp3_file in mp3_files:
    if (
        "_intro" not in mp3_file
        and "-intro" not in mp3_file
        and "_outro" not in mp3_file
    ):
        # get the duration of the current mp3 file
        tag = TinyTag.get(os.path.join(audio_folder_path, mp3_file))
        duration = tag.duration

        # get the corresponding story file
        story_files = [f for f in os.listdir(stories_folder_path) if f.endswith(".txt")]
        story_file = find_matching_story_file(mp3_file, story_files)

        print(f"Looking for story file for MP3: {mp3_file}")
        print(f"Found matching story file: {story_file}")

        if story_file:
            with open(os.path.join(stories_folder_path, story_file), "r") as f:
                story_data = json.load(f)

            print(f"Story data: {story_data}")

            # add a chapter with correct title and link
            chapters.append(
                {
                    "startTime": round(total_duration),
                    "title": story_data.get(
                        "title", f"Chapter {extract_number(mp3_file)}"
                    ),
                    "url": story_data.get("link", None),
                }
            )
        else:
            print(f"No matching story file found for {mp3_file}")
            # If no corresponding story file is found, add a generic chapter
            chapters.append(
                {
                    "startTime": round(total_duration),
                    "title": f"Chapter {extract_number(mp3_file)}",
                    "url": None,
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

print("Chapter file generated successfully.")
print(f"Final chapters: {chapters}")
