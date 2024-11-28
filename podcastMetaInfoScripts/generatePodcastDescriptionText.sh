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

html_output_file="$directory/podcastDescription.html"
txt_output_file="$directory/podcastDescription_formatted.txt"

# Extract the title from the directory name
title=$(basename "$directory")

# Initialize HTML and TXT data
html_data="Podcast Chapters\n"
txt_data="$title"$'\n'

# Process chapter information
chapter_file="$directory/chapters.json"
if [ -f "$chapter_file" ]; then
    # Use jq to parse JSON and format output
    chapters=$(jq -r '.chapters[] | "\(.startTime)|\(.title)|\(.url)"' "$chapter_file")
    
    while IFS='|' read -r start_time chapter_title url; do
        # Convert seconds to MM:SS format
        minutes=$(( start_time / 60 ))
        seconds=$(( start_time % 60 ))
        formatted_timestamp=$(printf "%02d:%02d" $minutes $seconds)

        if [ "$url" != "null" ]; then
            html_data+="        <p><strong><a href=\"#t=$formatted_timestamp\">$formatted_timestamp</a></strong> <a href=\"$url\">$chapter_title</a></p>\n"
            txt_data+="$formatted_timestamp $chapter_title - $url"$'\n'
        else
            html_data+="        <p><strong><a href=\"#t=$formatted_timestamp\">$formatted_timestamp</a></strong> $chapter_title</p>\n"
            txt_data+="$formatted_timestamp $chapter_title"$'\n'
        fi
    done <<< "$chapters"
else
    echo "Warning: Chapter file '$chapter_file' not found. Proceeding without chapter information."
fi

# Write the parsed data to the HTML output file
echo -e "$html_data" > "$html_output_file"

# Write the parsed data to the TXT output file
echo -e "$txt_data" > "$txt_output_file"

echo "Podcast description saved to $html_output_file"
echo "Simple formatted description saved to $txt_output_file"