#!/bin/zsh

create_env_files() {
    # Create .config.env file
    echo "## Environment variables" > .config.env
    echo "PODCAST_DATA_SOURCE_PLUGINS=hackerNewsAPIPlugin" >> .config.env
    echo "PODCAST_INTRO_PLUGINS=standardIntroPlugin" >> .config.env
    echo "PODCAST_SCRAPER_PLUGINS=newsStoryScraperPlugin" >> .config.env
    echo "PODCAST_SUMMARY_PLUGINS=storySummaryPlugin" >> .config.env
    echo "PODCAST_SEGMENT_WRITER_PLUGINS=topTenSegmentWriterPlugin" >> .config.env
    echo "PODCAST_OUTRO_PLUGINS=outroWriterPlugin" >> .config.env
    echo "PODCAST_PRODUCER_PLUGINS=producerPlugin" >> .config.env
    echo "" >> .config.env
    echo "# The following environment variables are for configuring the podcast for your specific needs" >> .config.env
    echo "# required" >> .config.env
    echo "PODCAST_NAME=$4" >> .config.env
    echo "PODCAST_TYPE=$5" >> .config.env
    echo "PODCAST_DESCRIPTION=$6" >> .config.env

    # Create .auth.env file
    echo "# Authentication and sensitive information" > .auth.env
    echo "OPENAI_API_KEY=$1" >> .auth.env
    echo "ANCHOR_EMAIL=$2" >> .auth.env
    echo "ANCHOR_PASSWORD=$3" >> .auth.env
}

main() {
    # Check if .config.env and .auth.env files already exist
    if [[ -f .config.env ]] || [[ -f .auth.env ]]; then
        echo ".config.env or .auth.env file already exists."
        exit 0
    fi

    # Prompt user for required information
    echo "Enter your OpenAI API Key: "
    read api_key
    echo "Enter your Anchor Email: "
    read anchor_email
    echo "Enter your Anchor Password: "
    read -s anchor_password
    echo "Enter your Podcast Name: "
    read podcast_name
    echo "Enter your Podcast Type: "
    read podcast_type
    echo "Enter your Podcast Description: "
    read podcast_description

    # Create .config.env and .auth.env files
    create_env_files "$api_key" "$anchor_email" "$anchor_password" "$podcast_name" "$podcast_type" "$podcast_description"
    echo ".config.env and .auth.env files created successfully."
}

main