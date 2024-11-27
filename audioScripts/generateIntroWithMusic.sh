#!/bin/zsh

# Check if enough arguments are passed
if [[ $# -ne 1 ]]; then
    echo "Usage: ./generateIntroWithMusic.sh <variable_directory_path>"
    exit 1
fi

# Retrieve the variable directory path parameter
variable_directory_path="$1"

# Variables for input files and output file
spoken_file="${variable_directory_path}/audio/0_intro.mp3"
backing_file="./audioScripts/podcast_intro_music.mp3"
output_file="${variable_directory_path}/audio/0_intro-withMusic.mp3"
temp_file="${variable_directory_path}/audio/temp_output.mp3"

# Ensure the audio directory exists
mkdir -p "${variable_directory_path}/audio/"

if [[ -f "$output_file" ]]; then
    echo "Error: Output file already exists at $output_file"
    exit 0
fi

# Check if input files exist and if output file already exists
if [[ ! -f "$spoken_file" ]]; then
    echo "Error: Spoken file not found at $spoken_file"
    exit 1
fi

if [[ ! -f "$backing_file" ]]; then
    echo "Error: Backing file not found at $backing_file"
    exit 1
fi

# Add 10 seconds of delay to the speech and fade out the music
ffmpeg -y -i "$backing_file" -i "$spoken_file" -filter_complex \
"[1]adelay=10000|10000[aud];[0]afade=t=out:st=10:d=5[bg];[bg][aud]amix=inputs=2" "$temp_file"

# Get the duration of the spoken audio
spoken_duration=$(ffprobe -i "$spoken_file" -show_entries format=duration -v quiet -of csv="p=0")

# Calculate the total duration (music + delay + spoken audio duration)
total_duration=$(echo "10 + $spoken_duration" | bc)

# Trim the output file to the length of the spoken audio
ffmpeg -y -i "$temp_file" -ss 0 -t "$total_duration" "$output_file"

# Cleanup
rm -f "$spoken_file" "$temp_file"