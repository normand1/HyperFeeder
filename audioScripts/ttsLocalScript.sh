#!/bin/zsh

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

# Function to convert text file to audio
convert_to_audio() {
  echo "Converting text to audio for file: $text_file"
  local text_file=$1
  local base_name=$(basename $text_file .txt)
  local audio_file="${AUDIO_DIR}${base_name}.aiff"
  local mp3_file="${AUDIO_DIR}${base_name}.mp3"

  # Read the text file and convert it to speech
  say -f $text_file -o $audio_file

  # Convert aiff to mp3
  ffmpeg -i $audio_file -f mp3 $mp3_file

  # Delete the aiff file after the mp3 file has been created
  rm $audio_file
}

# Process text files in the text directory
for text_file in $TEXT_DIR*.txt; do
  convert_to_audio $text_file
done

# Process text files in the intro_text directory
for text_file in $INTRO_TEXT_DIR*.txt; do
  convert_to_audio $text_file
done

# Process text files in the outro_text directory
for text_file in $OUTRO_TEXT_DIR*.txt; do
  convert_to_audio $text_file
done
