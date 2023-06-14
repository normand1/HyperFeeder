#!/bin/zsh

# Prompt user for configuration choice
echo -n "Enter configuration choice (news/podcast): "
read choice

# Define the new values based on the chosen configuration
if [[ "$choice" == "news" ]]; then
    NEW_PODCAST_DATA_SOURCE_PLUGINS=hackerNewsAPIPlugin
    NEW_PODCAST_INTRO_PLUGINS=standardIntroPlugin
    NEW_PODCAST_SCRAPER_PLUGINS=NewsStoryScraperPlugin
    NEW_PODCAST_SUMMARY_PLUGINS=storySummaryPlugin
    NEW_PODCAST_SEGMENT_WRITER_PLUGINS=topTenSegmentWriterPlugin
elif [[ "$choice" == "podcast" ]]; then
    NEW_PODCAST_DATA_SOURCE_PLUGINS=podcastFeedPlugin
    NEW_PODCAST_INTRO_PLUGINS=standardIntroPlugin
    NEW_PODCAST_SCRAPER_PLUGINS=RawScraperPlugin
    NEW_PODCAST_SUMMARY_PLUGINS=storySummaryPlugin
    NEW_PODCAST_SEGMENT_WRITER_PLUGINS=topTenSegmentWriterPlugin
else
    echo "Invalid choice. Exiting."
    exit 1
fi

# Update the .env file
sed -i '' "s/^PODCAST_DATA_SOURCE_PLUGINS=.*/PODCAST_DATA_SOURCE_PLUGINS=$NEW_PODCAST_DATA_SOURCE_PLUGINS/" .env
sed -i '' "s/^PODCAST_INTRO_PLUGINS=.*/PODCAST_INTRO_PLUGINS=$NEW_PODCAST_INTRO_PLUGINS/" .env
sed -i '' "s/^PODCAST_SCRAPER_PLUGINS=.*/PODCAST_SCRAPER_PLUGINS=$NEW_PODCAST_SCRAPER_PLUGINS/" .env
sed -i '' "s/^PODCAST_SUMMARY_PLUGINS=.*/PODCAST_SUMMARY_PLUGINS=$NEW_PODCAST_SUMMARY_PLUGINS/" .env
sed -i '' "s/^PODCAST_SEGMENT_WRITER_PLUGINS=.*/PODCAST_SEGMENT_WRITER_PLUGINS=$NEW_PODCAST_SEGMENT_WRITER_PLUGINS/" .env

echo "Configuration updated successfully."
