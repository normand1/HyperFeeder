#!/bin/zsh

# Check if enough arguments are passed
if [[ $# -ne 1 ]]; then
    echo "Usage: ./invoke_merge_audio.sh <variable_directory_path>"
    exit 1
fi

# Retrieve the variable directory path parameter
variable_directory_path="$1"

# Variables for input files and output file
spoken_file="${variable_directory_path}/audio/0_intro.mp3"
backing_file="./audioScripts/podcast_intro_music.mp3"
output_file="${variable_directory_path}/audio/0-intro-withMusic.mp3"

# Call the existing script with the hardcoded file paths
./audioScripts/merge_audio.sh "$spoken_file" "$backing_file" "$output_file"

# Cleanup
rm "$spoken_file"