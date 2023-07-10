#!/bin/zsh

# Prompt user for configuration choice
echo -n "Enter configuration choice\n (n) news | (p) podcasts | (nl) newsletter): "
read choice

# Define the new values based on the chosen configuration
if [[ "$choice" == "news" || "$choice" == "n" ]]; then
    NEW_PODCAST_DATA_SOURCE_PLUGINS=hackerNewsAPIPlugin
    NEW_PODCAST_INTRO_PLUGINS=standardIntroPlugin
    NEW_PODCAST_SCRAPER_PLUGINS=newsStoryScraperPlugin
    NEW_PODCAST_SUMMARY_PLUGINS=storySummaryPlugin
    NEW_PODCAST_SEGMENT_WRITER_PLUGINS=topTenSegmentWriterPlugin
    NEW_PODCAST_OUTRO_PLUGINS=funnyOutroWriterPlugin
    NEW_PODCAST_PRODUCER_PLUGINS=producerPlugin
elif [[ "$choice" == "podcasts" || "$choice" == "p" ]]; then
    echo -n "Enter the podcast RSS Feed: "
    read podcast_feed
    if grep -q "PODCAST_FEEDS=" podcastTextGenerationApp/podcastDataSourcePlugins/.env.datasource; then
        # If the variable exists in the file, replace it
        sed -i '' "s#^PODCAST_FEEDS=.*#PODCAST_FEEDS=$podcast_feed#" podcastTextGenerationApp/podcastDataSourcePlugins/.env.datasource
    else
        # If the variable doesn't exist in the file, add it
        echo "PODCAST_FEEDS=$podcast_feed" >> podcastTextGenerationApp/podcastDataSourcePlugins/.env.datasource
    fi
    echo -n "Enter the number of items to fetch: "
    read number_of_items
    if grep -q "NUMBER_OF_ITEMS_TO_FETCH=" podcastTextGenerationApp/podcastDataSourcePlugins/.env.datasource; then
        # If the variable exists in the file, replace it
        sed -i '' "s#^NUMBER_OF_ITEMS_TO_FETCH=.*#NUMBER_OF_ITEMS_TO_FETCH=$number_of_items#" podcastTextGenerationApp/podcastDataSourcePlugins/.env.datasource
    else
        # If the variable doesn't exist in the file, add it
        echo "NUMBER_OF_ITEMS_TO_FETCH=$number_of_items" >> podcastTextGenerationApp/podcastDataSourcePlugins/.env.datasource
    fi
    NEW_PODCAST_DATA_SOURCE_PLUGINS=podcastFeedPlugin
    NEW_PODCAST_INTRO_PLUGINS=standardIntroPlugin
    NEW_PODCAST_SCRAPER_PLUGINS=rawScraperPlugin
    NEW_PODCAST_SUMMARY_PLUGINS=storySummaryPlugin
    NEW_PODCAST_SEGMENT_WRITER_PLUGINS=topTenSegmentWriterPlugin
    NEW_PODCAST_OUTRO_PLUGINS=funnyOutroWriterPlugin
    NEW_PODCAST_PRODUCER_PLUGINS=producerPlugin
elif [[ "$choice" == "newsletter" || "$choice" == "nl" ]]; then
    echo -n "Enter the newsletter RSS Feed: "
    read newsletter_feed
    if grep -q "NEWSLETTER_RSS_FEEDS=" podcastTextGenerationApp/podcastDataSourcePlugins/.env.datasource; then
        # If the variable exists in the file, replace it
        sed -i '' "s#^NEWSLETTER_RSS_FEEDS=.*#NEWSLETTER_RSS_FEEDS=$newsletter_feed#" podcastTextGenerationApp/podcastDataSourcePlugins/.env.datasource
    else
        # If the variable doesn't exist in the file, add it
        echo "NEWSLETTER_RSS_FEEDS=$newsletter_feed" >> podcastTextGenerationApp/podcastDataSourcePlugins/.env.datasource
    fi
    echo -n "Enter the number of items to fetch: "
    read number_of_items
    if grep -q "NUMBER_OF_ITEMS_TO_FETCH=" podcastTextGenerationApp/podcastDataSourcePlugins/.env.datasource; then
        # If the variable exists in the file, replace it
        sed -i '' "s#^NUMBER_OF_ITEMS_TO_FETCH=.*#NUMBER_OF_ITEMS_TO_FETCH=$number_of_items#" podcastTextGenerationApp/podcastDataSourcePlugins/.env.datasource
    else
        # If the variable doesn't exist in the file, add it
        echo "NUMBER_OF_ITEMS_TO_FETCH=$number_of_items" >> podcastTextGenerationApp/podcastDataSourcePlugins/.env.datasource
    fi
    NEW_PODCAST_DATA_SOURCE_PLUGINS=newsletterRSSFeedPlugin
    NEW_PODCAST_INTRO_PLUGINS=standardIntroPlugin
    NEW_PODCAST_SCRAPER_PLUGINS=rssItemScraperPlugin
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
