# Podcast Producer Plugins

## Description
These plugins are used to organize the audiofiles of a podcast into the correct order (like a producer would before publishing). The plugin receives a list of all segments objects and the directories for the segments, intros and outro. This gives any plugin the context it needs to order the podcasts as desired. The ordering is accomplished by adding a number to the start of every file that will be used by the subsequent Text to speech generation and audio creation scripts.

## Protocol Requirements
Any new Producer Plugin must implement the methods of the `abstractProducerPlugin.py`.
The method `updateFileNames` must rename all of the files with a consistent numbered order in all directories passed via the parameters: `outroTextDirName`, `introDirName`, `segmentTextDirNameLambda`.

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