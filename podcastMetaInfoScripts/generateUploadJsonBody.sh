#!/bin/zsh

# Check if the directory argument is provided
if [ $# -ne 1 ]; then
  echo "Usage: $0 <directory>"
  exit 1
fi

# Directory where the file will be created
directory=$1

# Extract the last component of the directory
podcastTitle=$(basename "$directory")

# Define the JSON string
json="{\"audioFilePath\":\"../${directory}/final-podcast-to-upload.mp3\",\"podcastTitle\":\"${podcastTitle}\",\"podcastDescription\":\"The Autonomous Tech Podcast ${directory}\"}"

# Create the directory if it doesn't exist
mkdir -p "$directory"

# Define the output file path
outputFile="$directory/uploadJsonBody.json"

# Write the JSON string to the output file
echo "$json" > "$outputFile"

# Print a success message
echo "JSON string has been written to $outputFile."
echo "$json"