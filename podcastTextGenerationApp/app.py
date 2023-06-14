import os
import yaml
import json
import sys
import datetime

from dotenv import load_dotenv
from podcastScraperPlugins.utilities.newsScraper import NewsScraper
from podcastSummaryPlugins.utilities.storySummarizer import StorySummarizer
from podcastSegmentWriterPlugins.utilities.storySegmentWriter import StorySegmentWriter
from podcastIntroPlugins.utilities.podcastIntroWriter import PodcastIntroWriter
from pluginTypes import PluginType

from pluginManager import PluginManager

# TODO: Add this back in some time
# topStories.insert(0, {"title": "Presented by the Hypercatcher Podcast App", "link": "https://hypercatcher.com/", "hackerNewsRank": 0})


class App:
    def __init__(self):
        load_dotenv()
        self.pluginManager = PluginManager()
        self.dataSourcePlugins = self.pluginManager.load_plugins('./podcastTextGenerationApp/podcastDataSourcePlugins', PluginType.DATA_SOURCE)
        self.introPlugins = self.pluginManager.load_plugins('./podcastTextGenerationApp/podcastIntroPlugins', PluginType.INTRO)
        self.scraperPlugins = self.pluginManager.load_plugins('./podcastTextGenerationApp/podcastScraperPlugins', PluginType.SCRAPER)
        self.summarizerPlugins = self.pluginManager.load_plugins('./podcastTextGenerationApp/podcastSummaryPlugins', PluginType.SUMMARY)
        self.segmentWriterPlugins = self.pluginManager.load_plugins('./podcastTextGenerationApp/podcastSegmentWriterPlugins', PluginType.SEGMENT_WRITER)

    def run(self, podcastName):
        topStories = self.pluginManager.runDataSourcePlugins(self.dataSourcePlugins, podcastName)
        
        fileNameIntro = podcastName + "/intro_text/" + "intro.txt" 
        self.pluginManager.runIntroPlugins(self.introPlugins, topStories, os.environ['PODCAST_NAME'], fileNameIntro, os.environ['PODCAST_TYPE'])

        rawTextDirName = f"{podcastName}/raw_text/"
        summaryTextDirName = f"{podcastName}/summary_text/"
        segmentTextDirName = f"{podcastName}/segment_text/"
        fileName = lambda *params: f"{str(params[0])}-{params[1].split('/')[-2]}.txt"
        
        self.pluginManager.runStoryScraperPlugins(self.scraperPlugins, topStories, rawTextDirName, fileName)
        topStories = self.readFilesFromFolderIntoStories(rawTextDirName, "rawSplitText", topStories)

        self.pluginManager.runStorySummarizerPlugins(self.summarizerPlugins, topStories, summaryTextDirName, fileName)
        topStories = self.readFilesFromFolderIntoStories(summaryTextDirName, "summary", topStories)

        self.pluginManager.runStorySegmentWriterPlugins(self.segmentWriterPlugins, topStories, segmentTextDirName, fileName)

    def readFilesFromFolderIntoStories(self, folderPath, key, stories):
        for filename in os.listdir(folderPath):
            filePath = os.path.join(folderPath, filename)
            if os.path.isfile(filePath):
                fileText = open(filePath, 'r').read()
                pathParts = filePath.split('/')
                rank = pathParts[-1:][0].split('-')[0]
                index = next((index for index, item in enumerate(stories) if str(item['newsRank']) == rank), None)
                try:
                    stories[index][key] = json.loads(fileText)
                except:
                    stories[index][key] = fileText
        return stories
                
if __name__ == "__main__":
    app = App()
    if len(sys.argv) > 1:
        parameter = sys.argv[1]  # Get the first parameter passed to the script
        app.run(parameter)
    else:
        # Get current date and time
        current_datetime = datetime.datetime.now()

        # Format the date and time components
        month = current_datetime.strftime("%B")[:3]  # Get the month in abbreviated form
        day = current_datetime.strftime("%d")
        year = current_datetime.strftime("%Y")
        time = current_datetime.strftime("%I%p")

        # Generate the folder name
        folder_name = f"output/Podcast-{month}{day}-{year}-{time}"
        app.run(folder_name)