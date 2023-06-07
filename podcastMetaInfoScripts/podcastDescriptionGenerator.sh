#!/bin/zsh

# Check if the JSON file argument is provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 <output directory>"
    exit 1
fi

json_file="$1/chapters.json"

# Check if the JSON file exists
if [ ! -f "$json_file" ]; then
    echo "Error: JSON file '$json_file' not found."
    exit 1
fi

# Read JSON data from file
data=$(cat "$json_file")

# Parse JSON data using jq
parsed_data=$(echo "$data" | jq -r '.chapters[] | "(\(.startTime / 60 | floor):\(.startTime % 60 | round)) \(.title) - [\( .url)]"')

# Print the parsed data
echo "$parsed_data"
