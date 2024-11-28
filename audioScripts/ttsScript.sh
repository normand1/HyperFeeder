#!/bin/zsh

set -e

# Function to show usage
show_usage() {
    echo "Usage: $0 <directory> [-s|-i|-o]"
    echo "  -s: Process only segment text"
    echo "  -i: Process only intro text"
    echo "  -o: Process only outro text"
    echo "  If no flag is provided, all text types will be processed"
    exit 1
}

# Check for minimum arguments
if [ $# -lt 1 ]; then
    show_usage
fi

# First command line argument is the directory
DIR=$1
shift

# Parse flags
PROCESS_SEGMENT=true
PROCESS_INTRO=true
PROCESS_OUTRO=true

while getopts ":sio" opt; do
    case ${opt} in
        s )
            PROCESS_INTRO=false
            PROCESS_OUTRO=false
            ;;
        i )
            PROCESS_SEGMENT=false
            PROCESS_OUTRO=false
            ;;
        o )
            PROCESS_SEGMENT=false
            PROCESS_INTRO=false
            ;;
        \? )
            show_usage
            ;;
    esac
done

# Directory with your text files
TEXT_DIR="${DIR}/segment_text/"
INTRO_TEXT_DIR="${DIR}/intro_text/"
OUTRO_TEXT_DIR="${DIR}/outro_text/"

# Directory to store audio files
AUDIO_DIR="${DIR}/audio/"

# Create the audio directory if it doesn't exist
mkdir -p $AUDIO_DIR

# Function to convert text file to audio using Python script
convert_to_audio() {
    echo "using 3rd party TTS"
    local text_file=$1
    local base_name=$(basename $text_file .txt)
    local audio_file="${AUDIO_DIR}${base_name}.mp3"

    echo "Converting text to audio for file: $text_file"

    # Call the Python script
    if ! python3 audioScripts/convert_to_audio.py $text_file $audio_file; then
        echo "Failed to convert $text_file to audio."
        return 1
    fi
}

# Process text files based on flags
if $PROCESS_SEGMENT; then
    echo "Processing segment text files..."
    for text_file in $TEXT_DIR*.txt; do
        convert_to_audio $text_file || echo "Error processing $text_file"
    done
fi

if $PROCESS_INTRO; then
    echo "Processing intro text files..."
    for text_file in $INTRO_TEXT_DIR*.txt; do
        convert_to_audio $text_file || echo "Error processing $text_file"
    done
fi

if $PROCESS_OUTRO; then
    echo "Processing outro text files..."
    for text_file in $OUTRO_TEXT_DIR*.txt; do
        convert_to_audio $text_file || echo "Error processing $text_file"
    done
fi

echo "All requested files processed."