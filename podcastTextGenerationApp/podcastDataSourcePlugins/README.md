# Podcast Data Source Plugins

## Description
These plugins are used to identify sources of podcast segments that will used by subsequent plugins.

## Protocol Requirements
Any new Data Source Plugin must implement the methods of the `AbstractDataSourcePlugin.py`.
Most importantly this plugin must return a `List` of `PodcastStory` Objects. These story objects are passed in the AI prompt and provides important information about the story when writing the segment at the `podcastSegmentWriterPlugins` step. Your plugin can re-use one of the existing subclasses, or use the `PodcastStory` base class itself, but it may be useful to create your own subclass for your plugin to pass specific context about the story to the subsequent pipeline plugins.

## Pipeline Location

```
           +-------------------+
           | podcastDataSource | <---- HERE
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
           | podcastSegment   |
           |   WriterPlugins  |
           +-------------------+

```