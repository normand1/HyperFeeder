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
    echo "" >> .env
    echo "# New variables" >> .env
    echo "PODCAST_FEEDS=$7" >> .env
    echo "" >> .env
    echo "## Summarization plugin Variables" >> .env
    echo "MAX_SUMMARY_SEGMENTS=$8" >> .env
    echo "CHUNK_SIZE=$9" >> .env
    echo "OPENAI_MODEL_SUMMARY=${10}" >> .env
    echo "OPENAI_MAX_TOKENS_SUMMARY=${11}" >> .env
    echo "OPENAI_TEMPERATURE_SUMMARY=${12}" >> .env
}

main() {
    # Check if .env file already exists
    if [[ -f .env ]]; then
        echo ".env file already exists."
        exit 0
    fi

    # Prompt user for required information
    read "Enter your OpenAI API Key: " api_key
    read "Enter your Anchor Email: " anchor_email
    read "Enter your Anchor Password: " anchor_password
    read "Enter your Podcast Name: " podcast_name
    read "Enter your Podcast Type: " podcast_type
    read "Enter your Podcast Description: " podcast_description

    # Prompt user for new variables
    read "Enter your Podcast Feeds: " podcast_feeds
    read "Enter the maximum summary segments: " max_summary_segments
    read "Enter the chunk size: " chunk_size
    read "Enter the OpenAI model for summary: " openai_model_summary
    read "Enter the maximum tokens for summary: " openai_max_tokens_summary
    read "Enter the temperature for summary: " openai_temperature_summary

    # Create .env file
    create_env_file "$api_key" "$anchor_email" "$anchor_password" "$podcast_name" "$podcast_type" "$podcast_description" "$podcast_feeds" "$max_summary_segments" "$chunk_size" "$openai_model_summary" "$openai_max_tokens_summary" "$openai_temperature_summary"
    echo ".env file created successfully."
}

main
