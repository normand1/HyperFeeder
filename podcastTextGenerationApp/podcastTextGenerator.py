import os
import json
import sys
import datetime
from colorama import init, Fore, Style
from publicationPlanningManager import PublicationPlanningManager
from utilities.env_utils import parse_initial_query
import yaml  # Add this import at the top with other imports
import hashlib

init(autoreset=True)  # Initialize colorama

from dotenv import load_dotenv

from podcastSegmentWriterPlugins.utilities.utils import storyCouldNotBeScrapedText
from pluginTypes import PluginType
from pluginManager import PluginManager
from podcastDataSourcePlugins.models.story import Story
from podcastDataSourcePlugins.baseDataSourcePlugin import BaseDataSourcePlugin
from podcastDataSourcePlugins.tavilyDataSourcePlugin import TavilyDataSourcePlugin


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

    def run(
        self,
        podcastName,
        initialPlanningManager: PublicationPlanningManager = PublicationPlanningManager(),
        researchPlanningManager: PublicationPlanningManager = PublicationPlanningManager(),
        additionalAllowedPluginNamesForInitialResearch: list[str] = None,
    ):

        additionalAllowedPluginNamesForInitialResearch = additionalAllowedPluginNamesForInitialResearch or []
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

        def fileNameLambda(uniqueId, url=None):
            if url and "/" in url:
                return f"{str(uniqueId)}-{url.split('/')[-2]}.txt"
            else:
                return f"{str(uniqueId)}.txt"

        def researchFileNameLambda(uniqueId, url, researchType):
            if "/" in url:
                return f"{researchType}-{str(uniqueId)}-{url.split('/')[-2]}.txt"
            else:
                return f"{researchType}-{str(uniqueId)}-{url}.txt"

        if len(stories) == 0:
            print(f"{Fore.YELLOW}No stories found. Fetching new stories...{Style.RESET_ALL}")

            # Initial Research
            # Initial Publication Structure based on research
            # Replace the direct env access with the utility function
            queries = parse_initial_query()
            stories = []

            combinedAllowedPluginNamesForInitialResearch = [TavilyDataSourcePlugin.identify(simpleName=True)] + additionalAllowedPluginNamesForInitialResearch
            for query in queries:
                publicationStructure = initialPlanningManager.generatePublicationStructure(
                    query, list(self.dataSourcePlugins.values()), allowed_plugin_names=combinedAllowedPluginNamesForInitialResearch
                )
                print(f"{Fore.GREEN}{Style.BRIGHT}Publication structure:{Style.RESET_ALL}")
                print(publicationStructure)

                uniqueId = hashlib.md5(query.encode()).hexdigest()
                subStories = self.pluginManager.runDataSourcePlugins(publicationStructure, self.dataSourcePlugins, uniqueId, storyDirName, fileNameLambda)
                story = Story(newsRank=0, title=query, link="", storyType="Segment", uniqueId=uniqueId, source="")
                story.subStories = subStories
                # BaseDataSourcePlugin.writeToDisk(story, storyDirName, fileNameLambda)
                # stories = self.readStoriesFromFolder(storyDirName)
                if os.getenv("SHOULD_PAUSE_AND_VALIDATE_STORIES_BEFORE_SCRAPING", "false").lower() == "true":
                    self.pauseAndValidateStories(stories)
                researchQuery = f"based on what's been learned so far: ```{story.getCombinedSubStoryContext()}``` please use tools to look deeper into the initial question: ```{query}```"
                researchQueryUniqueId = hashlib.md5(researchQuery.encode()).hexdigest()
                researchPublicationStructure = researchPlanningManager.generatePublicationStructure(researchQuery, list(self.dataSourcePlugins.values()))
                research = self.pluginManager.runDataSourcePlugins(researchPublicationStructure, self.dataSourcePlugins, researchQueryUniqueId, researchDirName, researchFileNameLambda)
                # Update story.substories with research data
                mergedSubStories = {**story.subStories, **research}
                story.subStories = mergedSubStories
                stories.append(story)
                BaseDataSourcePlugin.writeToDisk(story, storyDirName, fileNameLambda)

        else:
            print(f"{Fore.GREEN}{Style.BRIGHT}Stories found:{Style.RESET_ALL}")
            for story in stories:
                print(f"{Fore.CYAN}{story.title}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}{Style.BRIGHT}Not running data source plugins.{Style.RESET_ALL}")
            stories = self.readStoriesFromFolder(storyDirName)

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

        for story in stories:
            # Create a filename for this story's filtered content
            story_filename = os.path.join(rawTextDirName, f"{story.uniqueId}_filtered_substories.yaml")

            for sourceKey, subStorySearchResults in story.subStories.items():
                for plugin in self.dataSourcePlugins.values():
                    aPlugin = plugin.plugin
                    if aPlugin.identify(simpleName=True) in sourceKey:
                        print(f"Found plugin {aPlugin.identify(simpleName=True)} for sub story source {sourceKey}")
                        seen_substories = set()
                        filteredSubStories = []
                        for searchResult in subStorySearchResults:
                            # Convert Story object to dict if necessary
                            resultToFilter = searchResult.to_dict() if isinstance(searchResult, Story) else searchResult
                            filteredSubStory = aPlugin.filterForImportantContextOnly(resultToFilter)

                            # Convert dict to a string representation for hashability
                            substory_str = json.dumps(filteredSubStory, sort_keys=True)
                            if substory_str not in seen_substories:
                                seen_substories.add(substory_str)
                                filteredSubStories.append(filteredSubStory)

                        story.subStories[sourceKey] = filteredSubStories  # replace with filtered sub stories

            # Ensure the directory exists
            os.makedirs(rawTextDirName, exist_ok=True)

            # Write the story data to a YAML file using the Story model's serialization
            with open(story_filename, "w", encoding="utf-8") as yaml_file:
                story_data = story.__json__()
                # Add raw text from filtered substories to rawSplitText
                raw_text = []
                for substories in story.subStories.values():
                    for substory in substories:
                        if isinstance(substory, dict) and "content" in substory:
                            raw_text.append(substory["content"])
                raw_split_text = "\n\n".join(raw_text)

                # Update both the story object and the story_data
                story.rawSplitText = raw_split_text
                story_data["rawSplitText"] = raw_split_text

                yaml.safe_dump(story_data, yaml_file, allow_unicode=True, default_flow_style=False)
                print(f"{Fore.GREEN}Wrote filtered sub-stories to {story_filename}{Style.RESET_ALL}")

        for story in stories:
            if hasattr(story, "rawSplitText"):
                if storyCouldNotBeScrapedText() in story.rawSplitText:  # This is default text added to a story if the story could not be scraped
                    print(f"{Fore.RED}{Style.BRIGHT}Error: A story could not be scraped.{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}{Style.BRIGHT}Error: A story does not have rawSplitText.{Style.RESET_ALL}")

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
