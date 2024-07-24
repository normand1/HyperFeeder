#!/bin/bash

# Load environment variables from .env file
if [ -f ./.env ]; then
    export $(grep -v '^#' ./.env | xargs)
else
    echo "Warning: .env file not found. Environment variables may not be set correctly."
fi

# Check if UPLOAD_ONLY is set, if not, set it to 0
if [ "$#" -lt 2 ]; then
    UPLOAD_ONLY=0
else
    UPLOAD_ONLY=$2
fi

# Generate a folder name if the user has not provided one
if [ "$#" -lt 1 ]; then
    FOLDER="output/Podcast-$(date +"%b%d-%Y-%I%p")"
else
    FOLDER="output/$1"
fi

# Generate Name without output folder
if [ "$#" -lt 1 ]; then
    FOLDERCLEAN="Podcast-$(date +"%b%d-%Y-%I%p")"
else
    FOLDERCLEAN="$1"
fi

# Create the folder regardless of UPLOAD_ONLY
mkdir -p ${FOLDER}

# Execute commands regardless of UPLOAD_ONLY
python podcastTextGenerationApp/app.py ${FOLDERCLEAN}
if [ "$?" -ne 0 ]; then
    echo "Error occurred during generating podcast text."
    exit 1
fi

./audioScripts/ttsLocalScript.sh ${FOLDER} 
if [ "$?" -ne 0 ]; then
    echo "Error occurred during generating podcast audio from text."
    exit 1
fi

./audioScripts/generateIntroWithMusic.sh "./${FOLDER}" 
if [ "$?" -ne 0 ]; then
    echo "Error occurred during generating intro with music."
    exit 1
fi

./audioScripts/combineAudioFiles.sh "./${FOLDER}" 
if [ "$?" -ne 0 ]; then
    echo "Error occurred during generating final podcast."
    exit 1
fi

python podcastTextGenerationApp/generatePodcastChapterFile.py ${FOLDER}
if [ "$?" -ne 0 ]; then
    echo "Error occurred during generating podcast chapters."
    exit 1
fi

./podcastMetaInfoScripts/generatePodcastDescriptionText.sh "./${FOLDER}" 
if [ "$?" -ne 0 ]; then
    echo "Error occurred during generating podcast description."
    exit 1
fi

./podcastMetaInfoScripts/generateUploadJsonBody.sh "${FOLDER}"
if [ "$?" -ne 0 ]; then
    echo "Error occurred during generateUploadJsonBody.sh."
    exit 1
fi

# Only perform upload if UPLOAD_ONLY is set to 1
if [ "$UPLOAD_ONLY" -eq 1 ]; then
    # Read the content from the file
    config=$(cat "./${FOLDER}/uploadJsonBody.json")
    echo "config: ${config}"
    npm --prefix install
    npm --prefix podcastUploader run upload -- "${config}"
    if [ "$?" -ne 0 ]; then
        echo "Error occurred during the upload process."
        exit 1
    fi
fi

# Print out a message if everything was successful
echo "All operations completed successfully."