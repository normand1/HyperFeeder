#!/bin/zsh

# Variables for input files and output file
spoken_file="$1"
backing_file="$2"
output_file="$3"

# Volume level for the backing track, 50 means it will be half as loud as the original
backing_track_volume=0.5

# Check if enough arguments are passed
if [[ $# -ne 3 ]]; then
    echo "Usage: ./merge_audio.sh <spoken_audio> <backing_track> <output_file>"
    exit 1
fi

# Check if the input files exist
if [[ ! -e "$spoken_file" ]]; then
    echo "Error: Spoken audio file doesn't exist: $spoken_file"
    exit 1
fi

if [[ ! -e "$backing_file" ]]; then
    echo "Error: Backing track file doesn't exist: $backing_file"
    exit 1
fi

# Temp file for the adjusted backing track
backing_adjusted="adjusted_backing.mp3"

# Adjust the volume of the backing track
ffmpeg -i "$backing_file" -af "volume=$backing_track_volume" "$backing_adjusted"

# Command to merge audio files using ffmpeg
ffmpeg -i "$spoken_file" -i "$backing_adjusted" -filter_complex amix=inputs=2:duration=longest "$output_file"

# Check if the output file was created successfully
if [[ -e "$output_file" ]]; then
    echo "Successfully created the output file: $output_file"
else
    echo "Error: Failed to create the output file"
    exit 1
fi

# Cleanup temporary file
rm "$backing_adjusted"
