#!/bin/zsh

# Prompt user for configuration choice
echo -n "Enter configuration choice (news | podcasts | newsletter): "
read choice

# Define the new values based on the chosen configuration
if [[ "$choice" == "news" ]]; then
    NEW_PODCAST_DATA_SOURCE_PLUGINS=hackerNewsAPIPlugin
    NEW_PODCAST_INTRO_PLUGINS=standardIntroPlugin
    NEW_PODCAST_SCRAPER_PLUGINS=NewsStoryScraperPlugin
    NEW_PODCAST_SUMMARY_PLUGINS=storySummaryPlugin
    NEW_PODCAST_SEGMENT_WRITER_PLUGINS=topTenSegmentWriterPlugin
    NEW_PODCAST_OUTRO_PLUGINS=funnyOutroWriterPlugin
    NEW_PODCAST_PRODUCER_PLUGINS=producerPlugin
elif [[ "$choice" == "podcasts" ]]; then
    echo -n "Enter the podcast RSS Feed: "
    read podcast_feed
    echo "PODCAST_FEEDS=$podcast_feed" >> .env
    NEW_PODCAST_DATA_SOURCE_PLUGINS=podcastFeedPlugin
    NEW_PODCAST_INTRO_PLUGINS=standardIntroPlugin
    NEW_PODCAST_SCRAPER_PLUGINS=RawScraperPlugin
    NEW_PODCAST_SUMMARY_PLUGINS=storySummaryPlugin
    NEW_PODCAST_SEGMENT_WRITER_PLUGINS=topTenSegmentWriterPlugin
    NEW_PODCAST_OUTRO_PLUGINS=funnyOutroWriterPlugin
    NEW_PODCAST_PRODUCER_PLUGINS=producerPlugin
elif [[ "$choice" == "newsletter" ]]; then
    echo -n "Enter the newsletter RSS Feed: "
    read newsletter_feed
    echo "NEWSLETTER_RSS_FEEDS=$newsletter_feed" >> .env
    NEW_PODCAST_DATA_SOURCE_PLUGINS=newsletterRSSFeedPlugin
    NEW_PODCAST_INTRO_PLUGINS=standardIntroPlugin
    NEW_PODCAST_SCRAPER_PLUGINS=RSSItemScraperPlugin
    NEW_PODCAST_SUMMARY_PLUGINS=storySummaryPlugin
    NEW_PODCAST_SEGMENT_WRITER_PLUGINS=topTenSegmentWriterPlugin
    NEW_PODCAST_OUTRO_PLUGINS=funnyOutroWriterPlugin
    NEW_PODCAST_PRODUCER_PLUGINS=producerPlugin
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
sed -i '' "s/^PODCAST_OUTRO_PLUGINS=.*/PODCAST_OUTRO_PLUGINS=$NEW_PODCAST_OUTRO_PLUGINS/" .env
sed -i '' "s/^PODCAST_PRODUCER_PLUGINS=.*/PODCAST_PRODUCER_PLUGINS=$NEW_PODCAST_PRODUCER_PLUGINS/" .env

echo "Configuration updated successfully."