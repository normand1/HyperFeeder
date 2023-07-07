# Podcast Segment Writer Plugins

## Description
These plugins are used to write segments that will be directly read during the podcast.

## Protocol Requirements
Any new Segment Writer Plugin must implement the methods of the `abstractSegmentWriterPlugin.py`.
The `Story` models are passed to this plugin via the `stories` parameter in the `writeStorySegment` function. The segment text should be written out to the directory identified by the `segmentTextDirNameLambda` parameter and the expected filename format for the raw text can be created by calling the segmemntTextFileNameLambda for each story with the story's `story["link"]` and `story["newsRank"]`. This ensures the name follows a standard that other plugins will use to identify the correct scraped text for a particular story.

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
           | podcastSummary   |
           |    Plugins       |
           +---------+---------+
                     |
                     |
           +---------v---------+
           | podcastSegment   | <---- HERE
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
           | podcastProducer   |
           |   Plugins         |
           +-------------------+

```