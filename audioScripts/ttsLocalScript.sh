#!/bin/zsh

set -e  # Exit immediately if a command exits with a non-zero status

# Function for logging
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1" >> "${DIR}/tts_debug.log"
}

# First command line argument is the directory
DIR=$1

# Directory with your text files
TEXT_DIR="${DIR}/segment_text/"
INTRO_TEXT_DIR="${DIR}/intro_text/"
OUTRO_TEXT_DIR="${DIR}/outro_text/"

# Directory to store audio files
AUDIO_DIR="${DIR}/audio/"

# Create the audio directory if it doesn't exist
mkdir -p $AUDIO_DIR

log "Script started. Working directory: $DIR"
log "Using Local TTS"

# Function to convert text file to audio
convert_to_audio() {
    local text_file=$1
    local base_name=$(basename $text_file .txt)
    local audio_file="${AUDIO_DIR}${base_name}.aiff"
    local mp3_file="${AUDIO_DIR}${base_name}.mp3"

    log "Converting text to audio for file: $text_file"

    if [ ! -f "$text_file" ]; then
        log "Error: Text file not found: $text_file"
        return 1
    fi

    # Read the text file and convert it to speech
    if ! say -f "$text_file" -o "$audio_file"; then
        log "Error: Failed to convert text to speech for $text_file"
        return 1
    fi

    # Convert aiff to mp3
    if ! ffmpeg -i "$audio_file" -f mp3 "$mp3_file" 2>> "${DIR}/tts_debug.log"; then
        log "Error: Failed to convert $audio_file to mp3"
        return 1
    fi

    # Delete the aiff file after the mp3 file has been created
    rm "$audio_file"

    log "Successfully created $mp3_file"
}

# Process text files in the text directories
for dir in "$TEXT_DIR" "$INTRO_TEXT_DIR" "$OUTRO_TEXT_DIR"; do
    log "Processing files in $dir"
    for text_file in "$dir"*.txt; do
        if [ -f "$text_file" ]; then
            if ! convert_to_audio "$text_file"; then
                log "Error processing $text_file"
            fi
        else
            log "No .txt files found in $dir"
        fi
    done
done

log "Script completed"