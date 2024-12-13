import datetime
import json
import os
import sys

from colorama import Fore, Style, init
from podcastDataSourcePlugins.models.segment import Segment
from toolUseManager import ToolUseManager
from utilities.env_utils import parse_initial_query

init(autoreset=True)  # Initialize colorama

from dotenv import load_dotenv
from pluginManager import PluginManager
from pluginTypes import PluginType
from podcastDataSourcePlugins.baseDataSourcePlugin import BaseDataSourcePlugin


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

        segments = []

        podcastName = podcastName.strip()
        load_dotenv(".config.env")
        storyDirName = f"output/{podcastName}/segments/"
        rawTextDirName = f"output/{podcastName}/raw_text/"
        segmentTextDirName = f"output/{podcastName}/segment_text/"
        fileNameIntro = f"output/{podcastName}/intro_text/intro.txt"
        directoryIntro = f"output/{podcastName}/intro_text/"
        fileNameOutro = f"output/{podcastName}/outro_text/outro.txt"
        directoryOutro = f"output/{podcastName}/outro_text/"

        print(f"{Fore.CYAN}{Style.BRIGHT}Starting podcast generation for: {podcastName}{Style.RESET_ALL}")
        segments = self.readSegmentsFromFolder(storyDirName)

        def fileNameLambda(uniqueId, url=None):
            if url and "/" in url:
                return f"{str(uniqueId)}-{url.split('/')[-2]}.txt"
            else:
                return f"{str(uniqueId)}.txt"

        if len(segments) == 0:
            print(f"{Fore.YELLOW}No segments found. Fetching new segments...{Style.RESET_ALL}")
            queries = parse_initial_query()
            segments = []

            if os.getenv("SHOULD_PAUSE_AND_VALIDATE_QUERIES_BEFORE_STARTING", "false").lower() == "true":
                self.pauseAndValidateStories(queries)

            for query in queries:
                previousSegmentText = ""
                previousToolsUsed = []
                mainSegment = Segment(title="", uniqueId="", sources={})

                for _ in range(2):
                    segmentResearchToolUseManager = ToolUseManager.toolUseManagerForSegmentResearch(query, self.dataSourcePlugins, previousSegmentText, previousToolsUsed)
                    partialSegment = self.pluginManager.runDataSourcePlugins(segmentResearchToolUseManager, self.dataSourcePlugins)

                    if not mainSegment.title:
                        mainSegment.title = partialSegment.title
                        mainSegment.uniqueId = partialSegment.uniqueId

                    # Merge partialSegment sources into mainSegment
                    for key, subs in partialSegment.sources.items():
                        if key not in mainSegment.sources:
                            mainSegment.sources[key] = subs
                        else:
                            mainSegment.sources[key].extend(subs)

                    # Update previousSegmentText from mainSegment after merging
                    segmentTextParts = [mainSegment.title]
                    for key, subs in mainSegment.sources.items():
                        for sub in subs:
                            if hasattr(sub, "content") and sub.content:
                                segmentTextParts.append(str(sub.content))
                    previousSegmentText = "\n".join(segmentTextParts)
                    previousToolsUsed = partialSegment.toolsUsed if hasattr(partialSegment, "toolsUsed") else []

                # After collecting all research into mainSegment, write once and add to segments
                BaseDataSourcePlugin.writeToDisk(mainSegment, storyDirName, fileNameLambda)
                segments.append(mainSegment)  # combine the segments together into a single segment

        else:
            print(f"{Fore.GREEN}{Style.BRIGHT}Stories found:{Style.RESET_ALL}")
            for segment in segments:
                print(f"{Fore.CYAN}{segment.title}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}{Style.BRIGHT}Not running data source plugins.{Style.RESET_ALL}")
            segments = self.readSegmentsFromFolder(storyDirName)

        # Ensure the directory exists once before processing
        os.makedirs(rawTextDirName, exist_ok=True)

        self.pluginManager.processSegments(segments, self.dataSourcePlugins, rawTextDirName)
        self.pluginManager.runStorySegmentWriterPlugins(self.segmentWriterPlugins, segments, segmentTextDirName, fileNameLambda)

        self.pluginManager.runIntroPlugins(
            self.introPlugins,
            segments,
            os.environ["PODCAST_NAME"],
            fileNameIntro,
            os.environ["PODCAST_TYPE"],
        )

        introText = self.getPreviouslyWrittenIntroText(fileNameIntro)

        self.pluginManager.runOutroWriterPlugins(
            self.outroWriterPlugins,
            segments,
            introText,
            fileNameOutro,
        )

        self.pluginManager.runPodcastProducerPlugins(
            self.producerPlugins,
            segments,
            directoryOutro,
            directoryIntro,
            segmentTextDirName,
            fileNameLambda,
        )

    def getPreviouslyWrittenIntroText(self, fileNameIntro):
        if os.path.exists(fileNameIntro):
            with open(fileNameIntro, "r", encoding="utf-8") as file:
                return file.read()
        return ""

    def readSegmentsFromFolder(self, folderPath):
        segments = []
        if not os.path.exists(folderPath) or not os.path.isdir(folderPath):
            return segments

        for filename in os.listdir(folderPath):
            filePath = os.path.join(folderPath, filename)
            if os.path.isfile(filePath):
                with open(filePath, "r", encoding="utf-8") as f:
                    fileText = f.read()
                    try:
                        story_dict = json.loads(fileText)
                        story = Segment.from_dict(story_dict)
                        segments.append(story)
                    except json.JSONDecodeError:
                        print(f"{Fore.RED}Error parsing JSON from {filename}{Style.RESET_ALL}")
        return segments

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

    def pauseAndValidateStories(self, queries: list[str]):
        print(f"{Fore.GREEN}{Style.BRIGHT}Queries that will be used to generate the podcast:{Style.RESET_ALL}")
        for query in queries:
            print(f"{Fore.CYAN}{query}{Style.RESET_ALL}")
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
