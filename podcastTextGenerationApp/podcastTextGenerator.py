import os
import json
import sys
import datetime
from colorama import init, Fore, Style

init(autoreset=True)  # Initialize colorama

from dotenv import load_dotenv
from podcastSegmentWriterPlugins.utilities.utils import storyCouldNotBeScrapedText
from pluginTypes import PluginType
from pluginManager import PluginManager
from podcastDataSourcePlugins.models.story import Story


class PodcastTextGenerator:
    def __init__(self):
        load_dotenv(".env")
        self.pluginManager = PluginManager()
        self.dataSourcePlugins = self.pluginManager.load_plugins(
            "./podcastTextGenerationApp/podcastDataSourcePlugins",
            PluginType.DATA_SOURCE,
        )
        self.researcherPlugins = self.pluginManager.load_plugins(
            "./podcastTextGenerationApp/podcastResearcherPlugins",
            PluginType.RESEARCHER,
        )
        self.introPlugins = self.pluginManager.load_plugins("./podcastTextGenerationApp/podcastIntroPlugins", PluginType.INTRO)
        self.scraperPlugins = self.pluginManager.load_plugins("./podcastTextGenerationApp/podcastScraperPlugins", PluginType.SCRAPER)
        self.segmentWriterPlugins = self.pluginManager.load_plugins(
            "./podcastTextGenerationApp/podcastSegmentWriterPlugins",
            PluginType.SEGMENT_WRITER,
        )
        self.outroWriterPlugins = self.pluginManager.load_plugins("./podcastTextGenerationApp/podcastOutroWriterPlugins", PluginType.OUTRO)
        self.producerPlugins = self.pluginManager.load_plugins("./podcastTextGenerationApp/podcastProducerPlugins", PluginType.PRODUCER)

    def run(self, podcastName):
        stories = []

        podcastName = podcastName.strip()
        load_dotenv(".config.env")
        storyDirName = f"output/{podcastName}/stories/"
        researchDirName = f"output/{podcastName}/research/"
        rawTextDirName = f"output/{podcastName}/raw_text/"
        segmentTextDirName = f"output/{podcastName}/segment_text/"
        fileNameIntro = f"output/{podcastName}/intro_text/intro.txt"
        directoryIntro = f"output/{podcastName}/intro_text/"
        fileNameOutro = f"output/{podcastName}/outro_text/outro.txt"
        directoryOutro = f"output/{podcastName}/outro_text/"

        print(f"{Fore.CYAN}{Style.BRIGHT}Starting podcast generation for: {podcastName}{Style.RESET_ALL}")
        stories = self.readStoriesFromFolder(storyDirName)
        research = self.readResearchFromFolder(researchDirName)

        def fileNameLambda(uniqueId, url):
            if "/" in url:
                return f"{str(uniqueId)}-{url.split('/')[-2]}.txt"
            else:
                return f"{str(uniqueId)}-{url}.txt"

        def researchFileNameLambda(uniqueId, url, researchType):
            if "/" in url:
                return f"{researchType}-{str(uniqueId)}-{url.split('/')[-2]}.txt"
            else:
                return f"{researchType}-{str(uniqueId)}-{url}.txt"

        if len(stories) == 0:
            print(f"{Fore.YELLOW}No stories found. Fetching new stories...{Style.RESET_ALL}")
            self.pluginManager.runDataSourcePlugins(self.dataSourcePlugins, storyDirName, fileNameLambda)
            stories = self.readStoriesFromFolder(storyDirName)
        else:
            print(f"{Fore.GREEN}{Style.BRIGHT}Stories found:{Style.RESET_ALL}")
            for story in stories:
                print(f"{Fore.CYAN}{story.title}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}{Style.BRIGHT}Not running data source plugins.{Style.RESET_ALL}")

        if len(research) == 0:
            self.pluginManager.runResearcherPlugins(self.researcherPlugins, storyDirName, fileNameLambda, stories, researchDirName, researchFileNameLambda)
        else:
            print(f"{Fore.GREEN}{Style.BRIGHT}Research found, not running researcher plugins.{Style.RESET_ALL}")

        self.pluginManager.runPodcastDataSourcePluginsWritePodcastDetails(self.dataSourcePlugins, podcastName, stories)
        if os.getenv("SHOULD_PAUSE_AND_VALIDATE_STORIES_BEFORE_SCRAPING", "false").lower() == "true":
            self.pauseAndValidateStories(stories)
        self.pluginManager.runIntroPlugins(
            self.introPlugins,
            stories,
            os.environ["PODCAST_NAME"],
            fileNameIntro,
            os.environ["PODCAST_TYPE"],
        )

        introText = self.getPreviouslyWrittenIntroText(fileNameIntro)

        self.pluginManager.runStoryScraperPlugins(self.scraperPlugins, stories, rawTextDirName, fileNameLambda, researchDirName)

        if len(stories) == 0:
            print(f"{Fore.RED}{Style.BRIGHT}ERROR: No stories found. Exiting.{Style.RESET_ALL}")
            sys.exit(0)

        stories = self.readFilesFromFolderIntoStories(rawTextDirName, "rawSplitText", stories)

        for story in stories:
            if not hasattr(story, "rawSplitText"):
                if storyCouldNotBeScrapedText() in story.rawSplitText:  # This is default text added to a story if the story could not be scraped
                    print(f"{Fore.RED}{Style.BRIGHT}Error: A story could not be scraped.{Style.RESET_ALL}")

        self.pluginManager.runStorySegmentWriterPlugins(self.segmentWriterPlugins, stories, segmentTextDirName, fileNameLambda)

        self.pluginManager.runOutroWriterPlugins(self.outroWriterPlugins, stories, introText, fileNameOutro)

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

    def readFilesFromFolderIntoStories(self, folderPath, key, stories: list[Story]) -> list[Story]:
        for filename in os.listdir(folderPath):
            if filename.endswith(".mp3") or filename.endswith(".srt"):
                continue
            filePath = os.path.join(folderPath, filename)
            if os.path.isfile(filePath):
                fileText = open(filePath, "r").read()
                pathParts = filePath.split("/")
                uniqueId = pathParts[-1:][0].split("-")[0]
                for index, story in enumerate(stories):
                    if story.uniqueId == uniqueId:
                        stories[index][key] = fileText
        return stories

    def readStoriesFromFolder(self, folderPath):
        stories = []
        if not os.path.exists(folderPath) or not os.path.isdir(folderPath):
            return stories

        for filename in os.listdir(folderPath):
            filePath = os.path.join(folderPath, filename)
            if os.path.isfile(filePath):
                with open(filePath, "r", encoding="utf-8") as f:
                    fileText = f.read()
                    try:
                        story_dict = json.loads(fileText)
                        story = Story.from_dict(story_dict)
                        stories.append(story)
                    except json.JSONDecodeError:
                        print(f"{Fore.RED}Error parsing JSON from {filename}{Style.RESET_ALL}")
        return stories

    def readResearchFromFolder(self, folderPath):
        research = []
        if not os.path.exists(folderPath) or not os.path.isdir(folderPath):
            return research

        for filename in os.listdir(folderPath):
            filePath = os.path.join(folderPath, filename)
            if os.path.isfile(filePath):
                with open(filePath, "r", encoding="utf-8") as f:
                    fileText = f.read()
                    try:
                        research_dict = json.loads(fileText)
                        research.append(research_dict)
                    except json.JSONDecodeError:
                        print(f"{Fore.RED}Error parsing JSON from {filename}{Style.RESET_ALL}")
        return research

    def pauseAndValidateStories(self, stories: list[Story]):
        print(f"{Fore.GREEN}{Style.BRIGHT}Stories found:{Style.RESET_ALL}")
        for story in stories:
            print(f"{Fore.CYAN}{story.title}{Style.RESET_ALL}")
        input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")


if __name__ == "__main__":
    app = PodcastTextGenerator()
    if len(sys.argv) > 1:
        parameter = sys.argv[1]  # Get the first parameter passed to the script
        print(f"{Fore.GREEN}Running with parameter: {parameter}{Style.RESET_ALL}")
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
        print(f"{Fore.GREEN}Running with generated folder name: {folder_name}{Style.RESET_ALL}")
        app.run(folder_name)
