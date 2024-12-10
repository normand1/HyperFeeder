# Podcast Outro Plugins

## Description
These plugins are used to write an outro segment for your podcast based on the content discussed. The plugin receives a list of all `segments` covered in segments as well as the intro text for the podcast so it can be referenced when writing the outro.

## Protocol Requirements
Any new Intro Plugin must implement the methods of the `abstractOutroPlugin.py`.
The method `writeOutro` must write the new outro segment to the directory passed into the plugin via the `outroTextDirName` parameter.

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
                     |
                     |
           +---------v---------+
           | podcastSegment   |<---- HERE
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