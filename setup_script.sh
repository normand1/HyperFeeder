#!/bin/zsh

create_env_file() {
    echo "# The following environment variables are required to generate the podcast" > .env
    echo "OPENAI_API_KEY=$1" >> .env
    echo "" >> .env
    echo "# The following environment variables are required to publish the podcast" >> .env
    echo "ANCHOR_EMAIL=$2" >> .env
    echo "ANCHOR_PASSWORD=$3" >> .env
    echo "" >> .env
    echo "# The following environment variables are for configuring the podcast for your specific needs" >> .env
    echo "# required" >> .env
    echo "PODCAST_NAME=$4" >> .env
    echo "PODCAST_TYPE=$5" >> .env
    echo "PODCAST_DESCRIPTION=$6" >> .env
}

main() {
    # Check if .env file already exists
    if [[ -f .env ]]; then
        echo ".env file already exists."
        exit 0
    fi

    # Prompt user for OpenAI API key
    read "api_key?Enter your OpenAI API Key: "

    # Prompt user for Anchor email
    read "anchor_email?Enter your Anchor Email: "

    # Prompt user for Anchor password
    read "anchor_password?Enter your Anchor Password: "

    # Prompt user for Podcast name
    read "podcast_name?Enter your Podcast Name: "

    # Prompt user for Podcast type
    read "podcast_type?Enter your Podcast Type: "

    # Prompt user for Podcast description
    read "podcast_description?Enter your Podcast Description: "

    # Create .env file with the API key
    create_env_file "$api_key" "$anchor_email" "$anchor_password" "$podcast_name" "$podcast_type" "$podcast_description"
    echo ".env file created successfully."
}

main
