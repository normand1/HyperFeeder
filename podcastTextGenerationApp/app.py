import os
import json
import sys
import datetime
from colorama import init, Fore, Back, Style

init(autoreset=True)  # Initialize colorama

from dotenv import load_dotenv
from pluginTypes import PluginType
from pluginManager import PluginManager


class App:
    def __init__(self):
        load_dotenv(".env")
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
        # Print the contents of .env file
        # print(f"{Fore.GREEN}Contents of .env file:{Style.RESET_ALL}")
        # with open(".env", "r") as env_file:
        #     for line in env_file:
        #         # Skip empty lines and comments
        #         if line.strip() and not line.strip().startswith("#"):
        #             print(line.strip())
        # print(f"{Fore.GREEN}End of .env file contents{Style.RESET_ALL}")
        load_dotenv(".env")
        storyDirName = f"output/{podcastName}/stories/"
        rawTextDirName = f"output/{podcastName}/raw_text/"
        segmentTextDirName = f"output/{podcastName}/segment_text/"
        fileNameIntro = f"output/{podcastName}/intro_text/intro.txt"
        directoryIntro = f"output/{podcastName}/intro_text/"
        fileNameOutro = f"output/{podcastName}/outro_text/outro.txt"
        directoryOutro = f"output/{podcastName}/outro_text/"

        print(
            f"{Fore.CYAN}{Style.BRIGHT}Starting podcast generation for: {podcastName}{Style.RESET_ALL}"
        )
        stories = self.readStoriesFromFolder(storyDirName)

        def fileNameLambda(uniqueId, url):
            if "/" in url:
                return f"{str(uniqueId)}-{url.split('/')[-2]}.txt"
            else:
                return f"{str(uniqueId)}-{url}.txt"

        if len(stories) == 0:
            print(
                f"{Fore.YELLOW}No stories found. Fetching new stories...{Style.RESET_ALL}"
            )
            self.pluginManager.runDataSourcePlugins(
                self.dataSourcePlugins, storyDirName, fileNameLambda
            )
            stories = self.readStoriesFromFolder(storyDirName)

        self.pluginManager.runPodcastDetailsPlugins(
            self.dataSourcePlugins, podcastName, stories
        )
        if os.environ["SHOULD_PAUSE_AND_VALIDATE_STORIES_BEFORE_SCRAPING"] == "true":
            self.pauseAndValidateStories(stories)
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

        if len(stories) == 0:
            print(
                f"{Fore.RED}{Style.BRIGHT}ERROR: No stories found. Exiting.{Style.RESET_ALL}"
            )
            sys.exit(0)

        stories = self.readFilesFromFolderIntoStories(
            rawTextDirName, "rawSplitText", stories
        )

        for story in stories:
            if "rawSplitText" in story:
                if "This story could not be scraped" in story["rawSplitText"]:
                    print(
                        f"{Fore.RED}{Style.BRIGHT}Error: A story could not be scraped.{Style.RESET_ALL}"
                    )
                    raise ValueError("This story could not be scraped")

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
            if filename.endswith(".mp3") or filename.endswith(".srt"):
                continue
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
                            print(
                                f"{Fore.RED}Error parsing JSON from {filename}{Style.RESET_ALL}"
                            )
        else:
            print(
                f"{Fore.YELLOW}Folder {folderPath} does not exist already, will be created...{Style.RESET_ALL}"
            )
        return stories

    def pauseAndValidateStories(self, stories):
        print(f"{Fore.GREEN}{Style.BRIGHT}Stories found:{Style.RESET_ALL}")
        for story in stories:
            print(f"{Fore.CYAN}{story['title']}{Style.RESET_ALL}")
        input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")


if __name__ == "__main__":
    app = App()
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
        print(
            f"{Fore.GREEN}Running with generated folder name: {folder_name}{Style.RESET_ALL}"
        )
        app.run(folder_name)
