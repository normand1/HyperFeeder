# Podcast Summary Plugins

## Description
These plugins are used to summarize raw text extracted from data sourced identified for the podcast that can be used by the segment writing plugin. 

## Protocol Requirements
Any new Summary Plugin must implement the methods of the `abstractStorySummaryPlugin.py`.
The `Story` models are passed to this plugin via the `topStories` parameter in the `summarizeText` function. The summary text should be written out to the directory identified by the `summaryTextDirName` parameter and the expected filename format for the raw text can be created by calling the `summaryTextFileNameLambda` for each story with the story's `story["link"]` and `story["newsRank"]`. This ensures the name follows a standard that other plugins will use to identify the correct summary text for a particular story.

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
           | podcastScraper   | 
           |    Plugins       |
           +---------+---------+
                     |
                     |
           +---------v---------+
           | podcastSummary   | <---- HERE
           |    Plugins       |
           +---------+---------+
                     |
                     |
           +---------v---------+
           | podcastSegment   | 
           |   WriterPlugins  |
           +-------------------+

```