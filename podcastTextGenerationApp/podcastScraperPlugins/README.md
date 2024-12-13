# Podcast Scraper Plugins

## Description
These plugins are used to scrape the data sources provided by the `PodcastStory` Data Models.

## Protocol Requirements
Any new Scraper Plugin must implement the methods of the `abstractStoryScraperPlugin.py`.
The `Story` models are passed to this plugin via the `segments` parameter in the `scrapeSiteForText` function. The scraped raw text should be written out to the directory identified by the `rawTextDirName` parameter and the expected filename format for the raw text can be created by calling the rawTextFileNameLambda for each story with the story's `story.link` and `story.newsRank`. This ensures the name follows a standard that other plugins will use to identify the correct scraped text for a particular story.

## Pipeline Location

```
           +-------------------+
           | podcastDataSource |
           |     Plugins       |
           +---------+---------+
                     |
                     |
           +---------v---------+
           | podcastIntro     | 
           |    Plugins       |
           +---------+---------+
                     |
                     |
           +---------v---------+
           | podcastScraper   | <---- HERE
           |    Plugins       |
           +---------+---------+
                     |
                     |
           +---------v---------+
           | podcastSummary   |
           |    Plugins       |
           +---------+---------+
                     |
                     |
           +---------v---------+
           | podcastSegment   |
           |   WriterPlugins  |
           +-------------------+
                     |
                     |
           +---------v---------+
           | podcastOutro     |
           |   WriterPlugins  |
           +-------------------+
                     |
                     |
           +---------v---------+
           | podcastProducer   |<---- HERE
           |   Plugins         |
           +-------------------+

```