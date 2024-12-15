import datetime
import json
import os
import sys

from colorama import Fore, Style, init
from dotenv import load_dotenv
from pluginManager import PluginManager
from pluginTypes import PluginType
from podcastDataSourcePlugins.baseDataSourcePlugin import BaseDataSourcePlugin
from podcastDataSourcePlugins.models.segment import FollowUp, Segment
from questionListManager import QuestionsAgent
from toolUseResearchAgent import ToolUseResearchAgent
from utilities.env_utils import parse_initial_query

init(autoreset=True)  # Initialize colorama


class PodcastTextGenerator:
    def __init__(self):
        load_dotenv(".env")
        self.pluginManager = PluginManager()
        self.dataSourcePlugins = self.pluginManager.load_plugins(
            "./podcastTextGenerationApp/podcastDataSourcePlugins",
            PluginType.DATA_SOURCE,
        )
        self.introPlugins = self.pluginManager.load_plugins("./podcastTextGenerationApp/podcastIntroPlugins", PluginType.INTRO)
        self.segmentWriterPlugins = self.pluginManager.load_plugins(
            "./podcastTextGenerationApp/podcastSegmentWriterPlugins",
            PluginType.SEGMENT_WRITER,
        )
        self.outroWriterPlugins = self.pluginManager.load_plugins("./podcastTextGenerationApp/podcastOutroWriterPlugins", PluginType.OUTRO)
        self.producerPlugins = self.pluginManager.load_plugins("./podcastTextGenerationApp/podcastProducerPlugins", PluginType.PRODUCER)

    # This is the main entry point for the podcast text generator
    def run(self, podcastName, initialQueryToolUseManager=None, questionListManagerCls=None):
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

        # Create the directory for storing the raw text files for building each segment
        os.makedirs(rawTextDirName, exist_ok=True)

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

            if os.getenv("SHOULD_PAUSE_AND_VALIDATE_QUERIES_BEFORE_STARTING", "false").lower() == "true":
                self.pauseAndValidateStories(queries)

            for query in queries:

                # Run the tool use research agent to get the segment
                toolUseResearchAgent = ToolUseResearchAgent.toolUseAgentForSegmentResearch(query, self.dataSourcePlugins, initialQueryToolUseManager)
                toolCallResponse = toolUseResearchAgent.invokeWithBoundToolsAndQuery()
                segment = self.pluginManager.runDataSourcePlugins(toolUseResearchAgent, toolCallResponse, self.dataSourcePlugins)

                # Run questions agent
                questionsAgent = QuestionsAgent.makeQuestionsAgent(segment.getCombinedSubStoryContext(), questionListManagerCls)
                followUpQuestions = questionsAgent.invoke()

                maxFollowUpQuestions = int(os.getenv("MAX_FOLLOW_UP_QUESTIONS"))
                for followUpQuery in followUpQuestions[:maxFollowUpQuestions]:
                    print(f"{Fore.YELLOW}Running follow-up question: {followUpQuery}{Style.RESET_ALL}")

                    # Run the tool use research agent to get the follow-up question research
                    toolUseResearchAgent = ToolUseResearchAgent.toolUseAgentForSecondaryResearch(followUpQuery, self.dataSourcePlugins, [], initialQueryToolUseManager)
                    toolCallResponse = toolUseResearchAgent.invokeWithBoundToolsAndQuery()
                    followUpQuestionSegment = self.pluginManager.runDataSourcePlugins(toolUseResearchAgent, toolCallResponse, self.dataSourcePlugins)

                    # Merge followUpQuestionSegment
                    for key, subs in followUpQuestionSegment.sources.items():
                        segment.sources.setdefault(key, []).extend(subs)

                    # Run the tool use research agent to get the follow-up question answer
                    followUpQueryAnswer = toolUseResearchAgent.handleFollowUpQuestionWithResearch(followUpQuery, followUpQuestionSegment)
                    segment.followUps.append(FollowUp(source=followUpQuestionSegment, question=followUpQuery, answer=followUpQueryAnswer))

                BaseDataSourcePlugin.writeToDisk(segment, storyDirName, fileNameLambda)
                segments.append(segment)

        else:
            print(f"{Fore.GREEN}{Style.BRIGHT}Stories found:{Style.RESET_ALL}")
            for segment in segments:
                print(f"{Fore.CYAN}{segment.title}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}{Style.BRIGHT}Not running data source plugins.{Style.RESET_ALL}")
            segments = self.readSegmentsFromFolder(storyDirName)

        # Cleanup and organize the segment text sources before sending to writing the segments, intro and outro
        self.pluginManager.processSegments(segments, self.dataSourcePlugins, rawTextDirName)

        # Write the Segment Text to disk
        segmentText = self.pluginManager.runStorySegmentWriterPlugins(self.segmentWriterPlugins, segments, segmentTextDirName, fileNameLambda)

        # Write the Intro Text to disk
        self.pluginManager.runIntroPlugins(
            self.introPlugins,
            segments,
            os.environ["PODCAST_NAME"],
            fileNameIntro,
            os.environ["PODCAST_TYPE"],
        )

        # Write the Outro Text to disk
        self.pluginManager.runOutroWriterPlugins(
            self.outroWriterPlugins,
            segments,
            fileNameIntro,
            fileNameOutro,
        )

        # Write the Podcast Meta Data to disk
        self.pluginManager.runPodcastProducerPlugins(
            self.producerPlugins,
            segments,
            directoryOutro,
            directoryIntro,
            segmentTextDirName,
            fileNameLambda,
        )

        if "genericTweetThreadWriter" in os.environ["PODCAST_SEGMENT_WRITER_PLUGINS"]:
            return segmentText

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
