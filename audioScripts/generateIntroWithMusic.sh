#!/bin/zsh
if [[ $# -ne 1 ]]; then
    echo "Usage: ./generateIntroWithMusic.sh <variable_directory_path>"
    exit 1
fi

variable_directory_path="$1"
spoken_file="${variable_directory_path}/audio/0_intro.mp3"
backing_file="./audioScripts/podcast_intro_music.mp3"
output_file="${variable_directory_path}/audio/0_intro-withMusic.mp3"
temp_file="${variable_directory_path}/audio/temp_output.mp3"

mkdir -p "${variable_directory_path}/audio/"
if [[ -f "$output_file" ]]; then
    echo "Error: Output file already exists at $output_file"
    exit 0
fi
if [[ ! -f "$spoken_file" ]]; then
    echo "Error: Spoken file not found at $spoken_file"
    exit 1
fi
if [[ ! -f "$backing_file" ]]; then
    echo "Error: Backing file not found at $backing_file"
    exit 1
fi

ffmpeg -y -i "$backing_file" -i "$spoken_file" \
-filter_complex "[1]adelay=10000|10000[aud];[0]afade=t=out:st=10:d=5[bg];[bg][aud]amix=inputs=2,loudnorm=I=-16:TP=-1.5:LRA=11[out]" \
-map "[out]" "$temp_file"

spoken_duration=$(ffprobe -i "$spoken_file" -show_entries format=duration -v quiet -of csv="p=0")
total_duration=$(echo "10 + $spoken_duration" | bc)

ffmpeg -y -i "$temp_file" -ss 0 -t "$total_duration" "$output_file"
rm -f "$spoken_file" "$temp_file"