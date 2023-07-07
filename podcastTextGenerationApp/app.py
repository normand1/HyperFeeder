import os
import json
import sys
import datetime

from dotenv import load_dotenv
from pluginTypes import PluginType
from pluginManager import PluginManager


class App:
    def __init__(self):
        load_dotenv()
        self.pluginManager = PluginManager()
        self.dataSourcePlugins = self.pluginManager.load_plugins(
            "./podcastTextGenerationApp/podcastDataSourcePlugins",
            PluginType.DATA_SOURCE,
        )
        self.introPlugins = self.pluginManager.load_plugins(
            "./podcastTextGenerationApp/podcastIntroPlugins", PluginType.INTRO
        )
        self.scraperPlugins = self.pluginManager.load_plugins(
            "./podcastTextGenerationApp/podcastScraperPlugins", PluginType.SCRAPER
        )
        self.summarizerPlugins = self.pluginManager.load_plugins(
            "./podcastTextGenerationApp/podcastSummaryPlugins", PluginType.SUMMARY
        )
        self.segmentWriterPlugins = self.pluginManager.load_plugins(
            "./podcastTextGenerationApp/podcastSegmentWriterPlugins",
            PluginType.SEGMENT_WRITER,
        )
        self.outroWriterPlugins = self.pluginManager.load_plugins(
            "./podcastTextGenerationApp/podcastOutroWriterPlugins", PluginType.OUTRO
        )
        self.producerPlugins = self.pluginManager.load_plugins(
            "./podcastTextGenerationApp/podcastProducerPlugins", PluginType.PRODUCER
        )

    def run(self, podcastName):
        stories = []

        storyDirName = f"output/{podcastName}/stories/"
        rawTextDirName = f"output/{podcastName}/raw_text/"
        summaryTextDirName = f"output/{podcastName}/summary_text/"
        segmentTextDirName = f"output/{podcastName}/segment_text/"
        fileNameIntro = f"output/{podcastName}/intro_text/intro.txt"
        directoryIntro = f"output/{podcastName}/intro_text/"
        fileNameOutro = f"output/{podcastName}/outro_text/outro.txt"
        directoryOutro = f"output/{podcastName}/outro_text/"

        stories = self.readStoriesFromFolder(storyDirName)

        def fileNameLambda(uniqueId, url):
            return f"{str(uniqueId)}-{url.split('/')[-2]}.txt"

        if len(stories) == 0:
            self.pluginManager.runDataSourcePlugins(
                self.dataSourcePlugins, storyDirName, fileNameLambda
            )
            stories = self.readStoriesFromFolder(storyDirName)

        self.pluginManager.runPodcastDetailsPlugins(
            self.dataSourcePlugins, podcastName, stories
        )
        self.pluginManager.runIntroPlugins(
            self.introPlugins,
            stories,
            os.environ["PODCAST_NAME"],
            fileNameIntro,
            os.environ["PODCAST_TYPE"],
        )

        introText = self.getPreviouslyWrittenIntroText(fileNameIntro)

        self.pluginManager.runStoryScraperPlugins(
            self.scraperPlugins, stories, rawTextDirName, fileNameLambda
        )
        stories = self.readFilesFromFolderIntoStories(
            rawTextDirName, "rawSplitText", stories
        )

        self.pluginManager.runStorySummarizerPlugins(
            self.summarizerPlugins, stories, summaryTextDirName, fileNameLambda
        )
        stories = self.readFilesFromFolderIntoStories(
            summaryTextDirName, "summary", stories
        )

        self.pluginManager.runStorySegmentWriterPlugins(
            self.segmentWriterPlugins, stories, segmentTextDirName, fileNameLambda
        )

        self.pluginManager.runOutroWriterPlugins(
            self.outroWriterPlugins, stories, introText, fileNameOutro
        )

        self.pluginManager.runPodcastProducerPlugins(
            self.producerPlugins,
            stories,
            directoryOutro,
            directoryIntro,
            segmentTextDirName,
            fileNameLambda,
        )

    def getPreviouslyWrittenIntroText(self, fileNameIntro):
        if os.path.exists(fileNameIntro):
            with open(fileNameIntro, "r") as file:
                return file.read()
        return ""

    def readFilesFromFolderIntoStories(self, folderPath, key, stories):
        for filename in os.listdir(folderPath):
            filePath = os.path.join(folderPath, filename)
            if os.path.isfile(filePath):
                fileText = open(filePath, "r").read()
                pathParts = filePath.split("/")
                uniqueId = pathParts[-1:][0].split("-")[0]
                for index, story in enumerate(stories):
                    if "uniqueId" in story and story["uniqueId"] == uniqueId:
                        stories[index][key] = fileText
        return stories

    def readStoriesFromFolder(self, folderPath):
        stories = []
        if os.path.exists(folderPath) and os.path.isdir(folderPath):
            for filename in os.listdir(folderPath):
                filePath = os.path.join(folderPath, filename)
                if os.path.isfile(filePath):
                    with open(filePath, "r") as f:
                        fileText = f.read()
                        try:
                            story = json.loads(fileText)
                            stories.append(story)
                        except json.JSONDecodeError:
                            print(f"Error parsing JSON from {filename}")
        else:
            print(f"Folder {folderPath} does not exist already, will be created...")
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
        folder_name = f"Podcast-{month}{day}-{year}-{time}"
        app.run(folder_name)
