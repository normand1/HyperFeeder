#!/bin/bash

# Generate a folder name if the user has not provided one
if [ "$#" -ne 1 ]; then
    FOLDER="output/Podcast-$(date +"%B%d-%Y-%I%p")"
else
    FOLDER="output/$1"
fi

# Create the new directory if it does not exist
mkdir -p ${FOLDER}

# Execute the scripts in sequence, waiting for each to complete before starting the next
python podcastTextGenerationApp/app.py ${FOLDER}
if [ "$?" -ne 0 ]; then
    echo "Error occurred during generating podcast text."
    exit 1
fi

./audioScripts/ttsScript.sh ${FOLDER} 
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

./podcastMetaInfoScripts/podcastDescriptionGenerator.sh "./${FOLDER}" 
if [ "$?" -ne 0 ]; then
    echo "Error occurred during generating podcast description."
    exit 1
fi

# Print out a message if everything was successful
echo "All operations completed successfully."
