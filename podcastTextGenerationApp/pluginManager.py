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

import json

from podcastDataSourcePlugins.models.story import Story
from utilities.textFilteringUtils import TextFilteringUtils
from podcastDataSourcePlugins.models.segment import Segment
from toolUseManager import ToolUseManager
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

    def runDataSourcePlugins(self, toolUseManager: ToolUseManager, plugins):
        subStories = {}
        toolCallResponse = toolUseManager.invokeWithBoundToolsAndQuery()
        message = self._extract_text_message(toolCallResponse)
        print(f"{Fore.GREEN}Tool call response: {message}{Style.RESET_ALL}")

        toolsUsed = []
        if hasattr(toolCallResponse, "tool_calls"):
            for toolCall in toolCallResponse.tool_calls:
                pluginName, function_name = toolCall["name"].split("-_-")
                # Find matching plugin
                matchingPlugin = next((plugin for plugin in plugins.values() if plugin.plugin.__class__.__name__ == pluginName), None)

                if matchingPlugin:
                    # Record the simple name of the plugin for excluding next time
                    simplePluginName = matchingPlugin.plugin.identify(simpleName=True)
                    if simplePluginName not in toolsUsed:
                        toolsUsed.append(simplePluginName)

                    plugin_function = getattr(matchingPlugin.plugin, function_name, None)
                    if plugin_function:
                        kwargs = {k: v for k, v in toolCall["args"].items()}
                        subStoryContent = plugin_function.invoke(kwargs)
                        for subStory in subStoryContent:
                            contentDict = matchingPlugin.plugin.fetchContentForStory(subStory)
                            subStory.content = contentDict
                        subStories[simplePluginName + toolUseManager.queryUniqueId] = subStoryContent
        else:
            print(f"{Fore.YELLOW}Warning: Plugin does not have attribute tool_calls {Style.RESET_ALL}")

        segment = Segment(title=toolUseManager.query, uniqueId=toolUseManager.queryUniqueId, sources=subStories)
        segment.toolsUsed = toolsUsed
        return segment

    def runResearcherPlugins(
        self,
        plugins,
        storiesDirName,
        storyFileNameLambda,
        segments: list[Story],
        researchDirName: str,
        researchFileNameLambda: str,
    ):
        # Sort plugins by priority
        sorted_plugins = sorted(plugins.items(), key=lambda x: x[1].plugin.priority)
        if len(sorted_plugins) == 0:
            raise Exception("No plugins to run Researcher Plugins")
        for name, plugin in sorted_plugins:
            if isinstance(plugin.plugin, BaseResearcherPlugin):
                print(f"Running Researcher Plugin: {plugin.plugin.identify()} (priority: {plugin.plugin.priority})")
                updatedStories = plugin.plugin.updateStories(segments)
                if updatedStories is not None:
                    for story in updatedStories:
                        # Overwrite the existing story with the updated story
                        plugin.plugin.writeToDisk(story, storiesDirName, storyFileNameLambda)
                research = plugin.plugin.researchStories(segments, researchDirName)
                if research is not None:
                    plugin.plugin.writeResearchToDisk(segments, research, researchDirName, researchFileNameLambda)
            else:
                print(f"Plugin {name} does not implement the necessary interface.")
        return segments

    def runPodcastDataSourcePluginsWritePodcastDetails(self, plugins, podcastName, segments):
        print("Running Data Source Plugins to write podcast details")
        if len(plugins.items()) == 0:
            raise Exception("No plugins to run Data Source Plugins to write podcast details")
        for name, plugin in plugins.items():
            if isinstance(plugin.plugin, BaseDataSourcePlugin):
                print(f"Running Data Source Plugins again to write podcast details: {plugin.plugin.identify()}")
                plugin.plugin.writePodcastDetails(f"output/{podcastName}", segments)

    def runIntroPlugins(self, plugins, segments, podcastName, introDirName, typeOfPodcast):
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

    def runStoryScraperPlugins(self, plugins, segments, rawTextDirName, rawTextFileNameLambda, researchDirName):
        print("Running Scraper Plugins")
        if len(plugins.items()) == 0:
            raise Exception("No plugins to run Scraper Plugins")
        for name, plugin in plugins.items():
            if isinstance(plugin.plugin, BaseStoryScraperPlugin):
                print(f"Running Scraper Plugins: {plugin.plugin.identify()}")
                for story in segments:
                    if not plugin.plugin.doesHandleStory(story):
                        print(f"Plugin {name} does not handle story {story.uniqueId}")
                        continue
                    if not plugin.plugin.doesOutputFileExist(story, rawTextDirName, rawTextFileNameLambda):
                        scrapedText = plugin.plugin.scrapeSiteForText(story, rawTextDirName)
                        if scrapedText is None:
                            print(f"Scraped text is None for scrapeSiteForText: {story.uniqueId}")

                        scrapedText = plugin.plugin.scrapeResearchAndOrganizeForSegmentWriter(story, rawTextDirName, researchDirName)

                        scrapedText = plugin.plugin.cleanupText(scrapedText)

                        plugin.plugin.writeToDisk(story, scrapedText, rawTextDirName, rawTextFileNameLambda)
            else:
                print(f"Plugin {name} does not implement the necessary interface.")

    def runStorySegmentWriterPlugins(self, plugins, segments, segmentTextDirNameLambda, segmentTextFileNameLambda):
        print("Running Segment Writer Plugins")
        if len(segments) == 0 or len(plugins.items()) == 0:
            raise Exception("No segments or plugins to run Segment Writer Plugins")
        for name, plugin in plugins.items():
            if isinstance(plugin.plugin, BaseSegmentWriterPlugin):
                print(f"Running Segment Plugins: {plugin.plugin.identify()}")
                for story in segments:
                    if not plugin.plugin.doesOutputFileExist(story, segmentTextDirNameLambda, segmentTextFileNameLambda):
                        segmentText = plugin.plugin.writeStorySegment(story, segments)
                        cleanSegmentText = TextFilteringUtils.cleanText(segmentText)
                        cleanSegmentText = TextFilteringUtils.remove_links(cleanSegmentText)
                        cleanSegmentText = TextFilteringUtils.cleanupStorySummary(cleanSegmentText)
                        plugin.plugin.writeToDisk(
                            story,
                            cleanSegmentText,
                            segmentTextDirNameLambda,
                            segmentTextFileNameLambda,
                        )
            else:
                print(f"Plugin {name} does not implement the necessary interface.")

    def runOutroWriterPlugins(self, plugins, segments, introText, outroTextDirName):
        for name, plugin in plugins.items():
            if isinstance(plugin.plugin, BaseOutroWriterPlugin):
                if not plugin.plugin.doesOutputFileExist(outroTextDirName):
                    print(f"Running Outro Plugins: {plugin.plugin.identify()}")
                    outroText = plugin.plugin.writeOutro(segments, introText)
                    plugin.plugin.writeToDisk(outroText, outroTextDirName)
            else:
                print(f"Plugin {name} does not implement the necessary interface.")

    def runPodcastProducerPlugins(
        self,
        plugins,
        segments,
        outroTextDirName,
        introDirName,
        segmentTextDirNameLambda,
        fileNameLambda,
    ):
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

        for story in segments:
            uniqueId = story.uniqueId
            url = hasattr(story, "link") and story.link or ""
            filename = fileNameLambda(uniqueId, url)
            filepath = os.path.join(stories_dir, filename)
            with open(filepath, "w") as file:
                dump_json(story, file, indent=2)
                file.flush()

        print(f"Updated segments written to {stories_dir}")

    def filterSubstories(self, segment, dataSourcePlugins):
        """Filter and deduplicate substories for each source in a segment."""
        for sourceKey, subStorySearchResults in segment.sources.items():
            for plugin in dataSourcePlugins.values():
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

                    segment.sources[sourceKey] = filteredSubStories  # replace with filtered sub segments

        return segment

    def processSegments(self, segments, dataSourcePlugins, rawTextDirName):
        os.makedirs(rawTextDirName, exist_ok=True)

        for segment in segments:
            story_filename = os.path.join(rawTextDirName, f"{segment.uniqueId}_filtered_substories.yaml")

            # Filter and deduplicate substories
            segment = self.filterSubstories(segment, dataSourcePlugins)

            # Extract raw text
            raw_text = [substory["content"] for substories in segment.sources.values() for substory in substories if isinstance(substory, dict) and "content" in substory]

            # Combine raw text and assign to segment
            raw_split_text = "\n\n".join(raw_text)
            segment.rawSplitText = raw_split_text

            # Serialize and add rawSplitText
            story_data = segment.__json__()
            story_data["rawSplitText"] = raw_split_text

            # Write YAML file
            with open(story_filename, "w", encoding="utf-8") as yaml_file:
                yaml.safe_dump(story_data, yaml_file, allow_unicode=True, default_flow_style=False)

            print(f"{Fore.GREEN}Wrote filtered sub-segments to {story_filename}{Style.RESET_ALL}")

            self._validateSegmentScraping(segment)

    def _validateSegmentScraping(self, segment):
        """Validates that all segments were properly scraped and have raw text content."""
        if hasattr(segment, "rawSplitText"):
            if storyCouldNotBeScrapedText() in segment.rawSplitText:  # This is default text added to a story if the story could not be scraped
                print(f"{Fore.RED}{Style.BRIGHT}Error: A story could not be scraped.{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}{Style.BRIGHT}Error: A story does not have rawSplitText.{Style.RESET_ALL}")

    def _extract_text_message(self, response):
        if hasattr(response, "content") and isinstance(response.content, list):
            for item in response.content:
                if isinstance(item, dict) and item.get("type") == "text":
                    return item.get("text", "")
        return ""
