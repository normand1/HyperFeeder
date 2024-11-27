#!/bin/zsh
rootDir=$1
dir="${rootDir}/audio"
echo "current directory: $PWD"
echo "looking in: $dir"
output_file="${rootDir}/final-podcast-to-upload.mp3"

# Get the sorted list of files
files=$(ls $dir/*.mp3 | sort -n)

# Read files into an array
files=("${(@f)files}")

# Write the list of files to a text file
for f in "${files[@]}"; do
    echo "file '$f'"
done > mylist.txt

# Concatenate the files
echo "rootDir: ${rootDir}"
echo "output_file: ${output_file}"
echo "Concatenate the files ${output_file}"
ffmpeg -f concat -safe 0 -i mylist.txt -acodec libmp3lame -b:a 128k "${output_file}"

# Clean up
rm mylist.txt