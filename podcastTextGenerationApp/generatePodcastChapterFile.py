#!/usr/bin/env python3
import os
import json
import re
from tinytag import TinyTag


class GeneratePodcastChapterFile:

    def main(self, folder_path):
        # the path to the folder containing your mp3 files
        audio_folder_path = os.path.join(folder_path, "audio")
        stories_folder_path = os.path.join(folder_path, "segments")

        # list to store the chapters
        chapters = []
        # counter for total duration
        total_duration = 0

        # create a list of mp3 files, sorted by the leading number
        mp3_files = sorted(
            [f for f in os.listdir(audio_folder_path) if f.endswith(".mp3")],
            key=self.extract_number,
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
            # get the duration of the current mp3 file
            tag = TinyTag.get(os.path.join(audio_folder_path, mp3_file))
            duration = tag.duration

            if "_intro" in mp3_file or "-intro" in mp3_file:
                chapters[0]["startTime"] = round(total_duration)
            elif "_outro" in mp3_file:
                chapters.append(
                    {
                        "startTime": round(total_duration),
                        "title": "Outro",
                        "url": None,
                    }
                )
            else:
                # get the corresponding story file
                story_files = [f for f in os.listdir(stories_folder_path) if f.endswith(".txt")]
                story_file = self.find_matching_story_file(mp3_file, story_files)

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
                            "title": story_data.get("title", f"Chapter {self.extract_number(mp3_file)}"),
                            "url": story_data.get("link", None),
                        }
                    )
                else:
                    print(f"No matching story file found for {mp3_file}")
                    # If no corresponding story file is found, add a generic chapter
                    chapters.append(
                        {
                            "startTime": round(total_duration),
                            "title": f"Chapter {self.extract_number(mp3_file)}",
                            "url": None,
                        }
                    )

            # Update total_duration for all files
            total_duration += duration

        # save the chapters to a json file
        with open(os.path.join(folder_path, "chapters.json"), "w") as f:
            json.dump({"version": "1.2.0", "chapters": chapters}, f)

        print("Chapter file generated successfully.")
        print(f"Final chapters: {chapters}")

    def extract_number(self, filename):
        match = re.match(r"(\d+)", filename)
        if match:
            return int(match.group(1))
        return 0  # Default to 0 if no number is found

    def find_matching_story_file(self, mp3_file, story_files):
        mp3_name = os.path.splitext(mp3_file)[0]
        for story_file in story_files:
            story_name = os.path.splitext(story_file)[0]
            if mp3_name.endswith(story_name) or story_name in mp3_name:
                return story_file
        return None
