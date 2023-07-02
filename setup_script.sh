#!/bin/zsh

create_env_file() {
    echo "## Environment variables" > .env
    echo "PODCAST_DATA_SOURCE_PLUGINS=hackerNewsAPIPlugin" >> .env
    echo "PODCAST_INTRO_PLUGINS=standardIntroPlugin" >> .env
    echo "PODCAST_SCRAPER_PLUGINS=NewsStoryScraperPlugin" >> .env
    echo "PODCAST_SUMMARY_PLUGINS=storySummaryPlugin" >> .env
    echo "PODCAST_SEGMENT_WRITER_PLUGINS=topTenSegmentWriterPlugin" >> .env
    echo "PODCAST_OUTRO_PLUGINS=funnyOutroWriterPlugin" >> .env
    echo "PODCAST_PRODUCER_PLUGINS=producerPlugin" >> .env
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
    echo "" >> .env
    echo "# Optional Plugin Variables" >> .env
    echo "PODCAST_FEEDS=" >> .env
    echo "NEWSLETTER_RSS_FEEDS=" >> .env
    echo "" >> .env
    echo "## Summarization plugin Variables" >> .env
    echo "MAX_SUMMARY_SEGMENTS=" >> .env
    echo "CHUNK_SIZE=" >> .env
    echo "OPENAI_MODEL_SUMMARY=" >> .env
    echo "OPENAI_MAX_TOKENS_SUMMARY=" >> .env
    echo "OPENAI_TEMPERATURE_SUMMARY=" >> .env
    echo "" >> .env
    echo "## Outro Writer Plugin Variables" >> .env
    echo "OPENAI_MAX_TOKENS_OUTRO=" >> .env
}

main() {
    # Check if .env file already exists
    if [[ -f .env ]]; then
        echo ".env file already exists."
        exit 0
    fi

    # Prompt user for required information
    echo "Enter your OpenAI API Key: "
    read api_key
    echo "Enter your Anchor Email: "
    read anchor_email
    echo "Enter your Anchor Password: "
    read anchor_password
    echo "Enter your Podcast Name: "
    read podcast_name
    echo "Enter your Podcast Type: "
    read podcast_type
    echo "Enter your Podcast Description: "
    read podcast_description

    # Create .env file
    create_env_file "$api_key" "$anchor_email" "$anchor_password" "$podcast_name" "$podcast_type" "$podcast_description"
    echo ".env file created successfully."
}

main