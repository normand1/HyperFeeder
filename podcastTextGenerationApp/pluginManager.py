import importlib.util
import json
import os

from pluginTypes import PluginType
from podcastDataSourcePlugins.baseDataSourcePlugin import BaseDataSourcePlugin
from podcastIntroPlugins.baseIntroPlugin import BaseIntroPlugin
from podcastOutroWriterPlugins.baseOutroWriterPlugin import BaseOutroWriterPlugin
from podcastProducerPlugins.BaseProducerPlugin import BaseProducerPlugin
from podcastResearcherPlugins.baseResearcherPlugin import BaseResearcherPlugin
from podcastScraperPlugins.baseStoryScraperPlugin import BaseStoryScraperPlugin
from podcastSegmentWriterPlugins.baseSegmentWriterPlugin import BaseSegmentWriterPlugin

from podcastDataSourcePlugins.models.story import Story


class PluginManager:
    # Loads the plugins from the given directory and returns a dictionary of the plugins
    def load_plugins(self, plugin_dir, plugin_type: PluginType):
        envVarName = f"PODCAST_{plugin_type.value}_PLUGINS"
        env_value = os.getenv(envVarName)
        if env_value is None:
            allowedPlugins = []
        elif "," in env_value:
            allowedPlugins = env_value.split(",")
        else:
            allowedPlugins = [env_value]

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

    def runDataSourcePlugins(self, plugins, storiesDirName, storyFileNameLambda):
        stories = []
        for name, plugin in plugins.items():
            if isinstance(plugin.plugin, BaseDataSourcePlugin):
                print(f"Running Data Source Plugins: {plugin.plugin.identify()}")
                fetchedStories = plugin.plugin.fetchStories()

                if fetchedStories is not None:
                    for story in fetchedStories:
                        if not plugin.plugin.doesOutputFileExist(story, storiesDirName, storyFileNameLambda):
                            plugin.plugin.writeToDisk(story, storiesDirName, storyFileNameLambda)
            else:
                print(f"Plugin {name} does not implement the necessary interface.")

        return stories

    def runResearcherPlugins(
        self,
        plugins,
        storiesDirName,
        storyFileNameLambda,
        stories: list[Story],
        researchDirName: str,
        researchFileNameLambda: str,
    ):
        # Sort plugins by priority
        sorted_plugins = sorted(plugins.items(), key=lambda x: x[1].plugin.priority)

        for name, plugin in sorted_plugins:
            if isinstance(plugin.plugin, BaseResearcherPlugin):
                print(f"Running Researcher Plugin: {plugin.plugin.identify()} (priority: {plugin.plugin.priority})")
                updatedStories = plugin.plugin.updateStories(stories)
                if updatedStories is not None:
                    for story in updatedStories:
                        # Overwrite the existing story with the updated story
                        plugin.plugin.writeToDisk(story, storiesDirName, storyFileNameLambda)
                research = plugin.plugin.researchStories(stories, researchDirName)
                if research is not None:
                    plugin.plugin.writeResearchToDisk(stories, research, researchDirName, researchFileNameLambda)
            else:
                print(f"Plugin {name} does not implement the necessary interface.")
        return stories

    def runPodcastDataSourcePluginsWritePodcastDetails(self, plugins, podcastName, stories):
        for name, plugin in plugins.items():
            if isinstance(plugin.plugin, BaseDataSourcePlugin):
                print(f"Running Data Source Plugins again to write podcast details: {plugin.plugin.identify()}")
                plugin.plugin.writePodcastDetails(f"output/{podcastName}", stories)

    def runIntroPlugins(self, plugins, stories, podcastName, introDirName, typeOfPodcast):
        for name, plugin in plugins.items():
            if isinstance(plugin.plugin, BaseIntroPlugin):
                print(f"Running Intro Plugins: {plugin.plugin.identify()}")
                if not plugin.plugin.doesOutputFileExist(introDirName):
                    introText = plugin.plugin.writeIntro(stories, podcastName, typeOfPodcast)
                    plugin.plugin.writeToDisk(introText, introDirName)
            else:
                print(f"Plugin {name} does not implement the necessary interface.")

    def runStoryScraperPlugins(self, plugins, stories, rawTextDirName, rawTextFileNameLambda, researchDirName):
        for name, plugin in plugins.items():
            if isinstance(plugin.plugin, BaseStoryScraperPlugin):
                print(f"Running Scraper Plugins: {plugin.plugin.identify()}")
                for story in stories:
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

    def runStorySegmentWriterPlugins(self, plugins, stories, segmentTextDirNameLambda, segmentTextFileNameLambda):
        for name, plugin in plugins.items():
            if isinstance(plugin.plugin, BaseSegmentWriterPlugin):
                print(f"Running Segment Plugins: {plugin.plugin.identify()}")
                for story in stories:
                    if not plugin.plugin.doesOutputFileExist(story, segmentTextDirNameLambda, segmentTextFileNameLambda):
                        segmentText = plugin.plugin.writeStorySegment(story, stories)
                        cleanSegmentText = plugin.plugin.cleanText(segmentText)
                        plugin.plugin.writeToDisk(
                            story,
                            cleanSegmentText,
                            segmentTextDirNameLambda,
                            segmentTextFileNameLambda,
                        )
            else:
                print(f"Plugin {name} does not implement the necessary interface.")

    def runOutroWriterPlugins(self, plugins, stories, introText, outroTextDirName):
        for name, plugin in plugins.items():
            if isinstance(plugin.plugin, BaseOutroWriterPlugin):
                if not plugin.plugin.doesOutputFileExist(outroTextDirName):
                    print(f"Running Outro Plugins: {plugin.plugin.identify()}")
                    outroText = plugin.plugin.writeOutro(stories, introText)
                    plugin.plugin.writeToDisk(outroText, outroTextDirName)
            else:
                print(f"Plugin {name} does not implement the necessary interface.")

    def runPodcastProducerPlugins(
        self,
        plugins,
        stories,
        outroTextDirName,
        introDirName,
        segmentTextDirNameLambda,
        fileNameLambda,
    ):
        for name, plugin in plugins.items():
            if isinstance(plugin.plugin, BaseProducerPlugin):
                print(f"Running Producer Plugins: {plugin.plugin.identify()}")
                stories = plugin.plugin.orderStories(stories)

                # Write updated stories back to disk
                self.writeStoriesToDisk(stories, fileNameLambda)

                plugin.plugin.updateFileNames(
                    stories,
                    outroTextDirName,
                    introDirName,
                    segmentTextDirNameLambda,
                    fileNameLambda,
                )
            else:
                print(f"Plugin {name} does not implement the necessary interface.")

    def writeStoriesToDisk(self, stories, fileNameLambda):
        stories_dir = "output/stories"  # Adjust this path as needed
        os.makedirs(stories_dir, exist_ok=True)

        for story in stories:
            uniqueId = story.uniqueId
            url = hasattr(story, "link") and story.link or ""
            filename = fileNameLambda(uniqueId, url)
            filepath = os.path.join(stories_dir, filename)
            with open(filepath, "w") as file:
                json.dump(story, file, indent=2)
                file.flush()

        print(f"Updated stories written to {stories_dir}")
