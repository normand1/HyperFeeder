#!/bin/zsh

create_env_file() {
    echo "## Environment variables" > .env
    echo "PODCAST_DATA_SOURCE_PLUGINS=hackerNewsAPIPlugin" >> .env
    echo "PODCAST_INTRO_PLUGINS=standardIntroPlugin" >> .env
    echo "PODCAST_SCRAPER_PLUGINS=NewsStoryScraperPlugin" >> .env
    echo "PODCAST_SEGMENT_WRITER_PLUGINS=topTenSegmentWriterPlugin" >> .env
    echo "PODCAST_SUMMARY_PLUGINS=storySummaryPlugin" >> .env
    echo "" >> .env
    echo "# The following environment variables are required to generate the podcast" >> .env
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

    # Prompt user for required information
    read "Enter your OpenAI API Key: "
    read "Enter your Anchor Email: "
    read "Enter your Anchor Password: "
    read "Enter your Podcast Name: "
    read "Enter your Podcast Type: "
    read "Enter your Podcast Description: "

    # Create .env file
    create_env_file "$api_key" "$anchor_email" "$anchor_password" "$podcast_name" "$podcast_type" "$podcast_description"
    echo ".env file created successfully."
}

main
