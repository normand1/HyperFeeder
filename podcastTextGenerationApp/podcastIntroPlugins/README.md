# Podcast Intro Plugins

## Description
These plugins are used to identify sources of podcast segments that will used by subsequent plugins.

## Protocol Requirements
Any new Intro Plugin must implement the methods of the `abstractIntroPlugin.py`.
The method `writeIntroSegment` must write the new intro segment to the directory passed into the plugin via the `fileNameIntro` parameter.

## Pipeline Location

```
           +-------------------+
           | podcastDataSource |
           |     Plugins       |
           +---------+---------+
                     |
                     |
           +---------v---------+
           | podcastIntro     | <---- HERE
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