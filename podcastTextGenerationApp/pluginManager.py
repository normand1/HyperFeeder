import importlib.util
import os
import yaml
from colorama import Fore, Style
from pluginTypes import PluginType
from podcastDataSourcePlugins.baseDataSourcePlugin import BaseDataSourcePlugin
from podcastIntroPlugins.baseIntroPlugin import BaseIntroPlugin
from podcastOutroWriterPlugins.baseOutroWriterPlugin import BaseOutroWriterPlugin
from podcastProducerPlugins.BaseProducerPlugin import BaseProducerPlugin
from podcastResearcherPlugins.baseResearcherPlugin import BaseResearcherPlugin
from podcastScraperPlugins.baseStoryScraperPlugin import BaseStoryScraperPlugin
from podcastSegmentWriterPlugins.baseSegmentWriterPlugin import BaseSegmentWriterPlugin
from json_utils import dump_json
from langchain_core.messages import BaseMessage

import json

from podcastDataSourcePlugins.models.story import Story
from utilities.textFilteringUtils import TextFilteringUtils
from podcastDataSourcePlugins.models.segment import Segment
from toolUseResearchAgent import ToolUseResearchAgent
from podcastSegmentWriterPlugins.utilities.utils import storyCouldNotBeScrapedText


class PluginManager:
    # Loads the plugins from the given directory and returns a dictionary of the plugins
    def load_plugins(self, plugin_dir, plugin_type: PluginType):
        envVarName = f"PODCAST_{plugin_type.value}_PLUGINS"
        env_value = os.getenv(envVarName)
        if env_value is None:
            allowedPlugins = []
        elif "," in env_value:
            allowedPlugins = [p.strip("\"'") for p in env_value.split(",")]
        else:
            allowedPlugins = [env_value.strip("\"'")]

        plugins = {}
        for filename in os.listdir(plugin_dir):
            if filename.endswith(".py"):
                name = filename[:-3]
                if name in allowedPlugins:
                    spec = importlib.util.spec_from_file_location(name, os.path.join(plugin_dir, filename))
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    plugins[name] = module
        return plugins

    def runDataSourcePlugins(self, toolUseResearchAgent: ToolUseResearchAgent, toolCallResponse: BaseMessage, plugins):
        sources = {}
        message = self.extract_text_message(toolCallResponse)
        print(f"{Fore.GREEN}Tool call response: {message}{Style.RESET_ALL}")

        toolsUsed = []
        if hasattr(toolCallResponse, "tool_calls"):
            for toolCall in toolCallResponse.tool_calls:
                pluginName, function_name = toolCall["name"].split("-_-")
                # Find matching plugin
                matchingPlugin = next((plugin for plugin in plugins.values() if plugin.plugin.__class__.__name__ == pluginName), None)
                simplePluginName = matchingPlugin.plugin.identify(simpleName=True)
                plugin_function = getattr(matchingPlugin.plugin, function_name, None)
                if plugin_function:
                    kwargs = {k: v for k, v in toolCall["args"].items()}
                    subStoryContent = plugin_function.invoke(kwargs)
                    for subStory in subStoryContent:
                        contentDict = matchingPlugin.plugin.fetchContentForStory(subStory)
                        subStory.content = contentDict
                    sources[simplePluginName + toolUseResearchAgent.queryUniqueId] = subStoryContent
        else:
            print(f"{Fore.YELLOW}Warning: Plugin does not have attribute tool_calls {Style.RESET_ALL}")

        segment = Segment(title=toolUseResearchAgent.query, uniqueId=toolUseResearchAgent.queryUniqueId, sources=sources)
        segment.toolsUsed = toolsUsed
        return segment

    def runIntroPlugins(self, plugins, segments, podcastName, introDirName, typeOfPodcast):
        if "genericNewsPodcastSegmentWriter" not in os.environ["PODCAST_SEGMENT_WRITER_PLUGINS"]:
            print(f"{Fore.RED}Skipping Intro Plugins{Style.RESET_ALL}")
            return
        print("Running Intro Plugins")
        if len(plugins.items()) == 0:
            raise Exception("No plugins to run Intro Plugins")
        for name, plugin in plugins.items():
            if isinstance(plugin.plugin, BaseIntroPlugin):
                print(f"Running Intro Plugins: {plugin.plugin.identify()}")
                if not plugin.plugin.doesOutputFileExist(introDirName):
                    introText = plugin.plugin.writeIntro(segments, podcastName, typeOfPodcast)
                    plugin.plugin.writeToDisk(introText, introDirName)
            else:
                print(f"Plugin {name} does not implement the necessary interface.")

    def runStorySegmentWriterPlugins(self, plugins, segments, segmentTextDirNameLambda, segmentTextFileNameLambda):
        print("Running Segment Writer Plugins")
        if len(segments) == 0 or len(plugins.items()) == 0:
            raise Exception("No segments or plugins to run Segment Writer Plugins")
        for name, plugin in plugins.items():
            if isinstance(plugin.plugin, BaseSegmentWriterPlugin):
                print(f"Running Segment Plugins: {plugin.plugin.identify()}")
                for segment in segments:
                    if not plugin.plugin.doesOutputFileExist(segment, segmentTextDirNameLambda, segmentTextFileNameLambda):
                        segmentText = plugin.plugin.writeStorySegment(segment, segments)
                        plugin.plugin.writeToDisk(
                            segment,
                            segmentText,
                            segmentTextDirNameLambda,
                            segmentTextFileNameLambda,
                        )
                        return segmentText
            else:
                print(f"Plugin {name} does not implement the necessary interface.")

    def runOutroWriterPlugins(self, plugins, segments, fileNameIntro, outroTextDirName):
        if "genericNewsPodcastSegmentWriter" not in os.environ["PODCAST_SEGMENT_WRITER_PLUGINS"]:
            print(f"{Fore.RED}Skipping Outro Plugins{Style.RESET_ALL}")
            return
        introText = self.getPreviouslyWrittenIntroText(fileNameIntro)
        for name, plugin in plugins.items():
            if isinstance(plugin.plugin, BaseOutroWriterPlugin):
                if not plugin.plugin.doesOutputFileExist(outroTextDirName):
                    print(f"Running Outro Plugins: {plugin.plugin.identify()}")
                    outroText = plugin.plugin.writeOutro(segments, introText)
                    plugin.plugin.writeToDisk(outroText, outroTextDirName)
            else:
                print(f"Plugin {name} does not implement the necessary interface.")

    def getPreviouslyWrittenIntroText(self, fileNameIntro):
        if os.path.exists(fileNameIntro):
            with open(fileNameIntro, "r", encoding="utf-8") as file:
                return file.read()
        return ""

    def runPodcastProducerPlugins(
        self,
        plugins,
        segments,
        outroTextDirName,
        introDirName,
        segmentTextDirNameLambda,
        fileNameLambda,
    ):
        if "genericNewsPodcastSegmentWriter" not in os.environ["PODCAST_SEGMENT_WRITER_PLUGINS"]:
            print(f"{Fore.RED}Skipping Producer Plugins{Style.RESET_ALL}")
            return
        for name, plugin in plugins.items():
            if isinstance(plugin.plugin, BaseProducerPlugin):
                print(f"Running Producer Plugins: {plugin.plugin.identify()}")
                segments = plugin.plugin.orderStories(segments)

                # Write updated segments back to disk
                self.writeStoriesToDisk(segments, fileNameLambda)

                plugin.plugin.updateFileNames(
                    segments,
                    outroTextDirName,
                    introDirName,
                    segmentTextDirNameLambda,
                    fileNameLambda,
                )
            else:
                print(f"Plugin {name} does not implement the necessary interface.")

    def writeStoriesToDisk(self, segments, fileNameLambda):
        stories_dir = "output/segments"  # Adjust this path as needed
        os.makedirs(stories_dir, exist_ok=True)

        for segment in segments:
            uniqueId = segment.uniqueId
            url = hasattr(segment, "link") and segment.link or ""
            filename = fileNameLambda(uniqueId, url)
            filepath = os.path.join(stories_dir, filename)
            with open(filepath, "w", encoding="utf-8") as file:
                dump_json(segment, file, indent=2)
                file.flush()

        print(f"Updated segments written to {stories_dir}")

    def filterSubstories(self, segment, dataSourcePlugins):
        """Filter and deduplicate substories for each source in a segment."""
        for sourceKey, subStorySearchResults in segment.sources.items():
            for plugin in dataSourcePlugins.values():
                aPlugin = plugin.plugin
                if aPlugin.identify(simpleName=True) in sourceKey:
                    print(f"Found plugin {aPlugin.identify(simpleName=True)} for sub segment source {sourceKey}")
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

                    segment.sources[sourceKey] = filteredSubStories  # replace with filtered sub segments

        return segment

    def processSegments(self, segments, dataSourcePlugins, rawTextDirName):
        os.makedirs(rawTextDirName, exist_ok=True)

        for segment in segments:
            story_filename = os.path.join(rawTextDirName, f"{segment.uniqueId}_filtered_substories.yaml")

            # Filter and deduplicate substories
            segment = self.filterSubstories(segment, dataSourcePlugins)

            # Extract raw text from substories
            raw_story_text = [substory["content"] for substories in segment.sources.values() for substory in substories if isinstance(substory, dict) and "content" in substory]
            raw_follow_up_text = [followUp.answer for followUp in segment.followUps]
            # Combine raw text and assign to segment
            raw_split_text = "Story Text: \n".join(raw_story_text) + "\nAdditional Research: \n".join(raw_follow_up_text)
            segment.rawSplitText = raw_split_text

            # Write YAML file
            with open(story_filename, "w", encoding="utf-8") as yaml_file:
                yaml.safe_dump(segment, yaml_file, allow_unicode=True, default_flow_style=False)

            print(f"{Fore.GREEN}Wrote filtered sub-segments to {story_filename}{Style.RESET_ALL}")

            self._validateSegmentScraping(segment)

    def _validateSegmentScraping(self, segment):
        """Validates that all segments were properly scraped and have raw text content."""
        if hasattr(segment, "rawSplitText"):
            if storyCouldNotBeScrapedText() in segment.rawSplitText:  # This is default text added to a segment if the segment could not be scraped
                print(f"{Fore.RED}{Style.BRIGHT}Error: A segment could not be scraped.{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}{Style.BRIGHT}Error: A segment does not have rawSplitText.{Style.RESET_ALL}")

    def extract_text_message(self, response):
        if hasattr(response, "content") and isinstance(response.content, list):
            for item in response.content:
                if isinstance(item, dict) and item.get("type") == "text":
                    return item.get("text", "")
        return ""
