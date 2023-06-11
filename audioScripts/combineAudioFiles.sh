#!/bin/zsh

rootDir=$1
dir="${rootDir}/audio"
echo "current directory: $PWD"
echo "looking in: $dir"
output_file="${rootDir}/final-podcast-to-upload.mp3"
fade_duration=1  # fade duration in seconds, adjust as needed

# Get the sorted list of files
files=$(ls $dir/*.mp3 | sort -n)

# Read files into an array
files=("${(@f)files}")

# Get duration of the first track
first_duration=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "${files[1]}")

# Apply a fade-out to the end of the first track
ffmpeg -i "${files[1]}" -af "afade=t=out:st=$(bc <<< "$first_duration - $fade_duration"):d=$fade_duration" "${dir}/1_fadeout.mp3"

# Apply a fade-in to the start of the second track
ffmpeg -i "${files[2]}" -af "afade=t=in:st=0:d=$fade_duration" "${dir}/2_fadein.mp3"

# Replace the original first and second tracks with the modified versions in the list
files[1]="${dir}/1_fadeout.mp3"
files[2]="${dir}/2_fadein.mp3"

# Write the list of files to a text file
for f in "${files[@]}"; do
    echo "file '$f'"
done > mylist.txt

# Concatenate the files
echo "rootDir: ${rootDir}"
echo "output_file: ${output_file}"
echo "Concatenate the files ${output_file}"
ffmpeg -f concat -safe 0 -i mylist.txt -c copy "${output_file}"

# Clean up
rm mylist.txt "${dir}/1_fadeout.mp3" "${dir}/2_fadein.mp3"
