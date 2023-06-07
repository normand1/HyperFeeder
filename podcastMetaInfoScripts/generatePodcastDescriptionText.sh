#!/bin/zsh

# Check if the directory argument is provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 <directory>"
    exit 1
fi

directory="$1"

# Check if the directory exists
if [ ! -d "$directory" ]; then
    echo "Error: Directory '$directory' not found."
    exit 1
fi

json_file="$directory/chapters.json"
output_file="$directory/podcastDescription.txt"

# Check if the JSON file exists
if [ ! -f "$json_file" ]; then
    echo "Error: JSON file '$json_file' not found."
    exit 1
fi

# Read JSON data from file
data=$(cat "$json_file")

# Parse JSON data using jq and round the time values
parsed_data=$(echo "$data" | jq -r '.chapters[] | "(\(.startTime / 60 | round):\(.startTime % 60 | round)) \(.title) - [\(.url)]"')

# Write the parsed data to the output file
echo "$parsed_data" > "$output_file"

echo "podcast description saved to $output_file"
