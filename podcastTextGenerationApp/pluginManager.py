import os
import importlib.util
from podcastDataSourcePlugins.baseDataSourcePlugin import BaseDataSourcePlugin
from podcastIntroPlugins.baseIntroPlugin import BaseIntroPlugin
from podcastScraperPlugins.baseStoryScraperPlugin import BaseStoryScraperPlugin
from podcastSummaryPlugins.baseSummaryPlugin import BaseSummaryPlugin
from podcastSegmentWriterPlugins.baseSegmentWriterPlugin import BaseSegmentWriterPlugin
from podcastOutroWriterPlugins.baseOutroWriterPlugin import BaseOutroWriterPlugin
from podcastProducerPlugins.BaseProducerPlugin import BaseProducerPlugin
from dotenv import load_dotenv
from pluginTypes import PluginType


class PluginManager:
    def load_plugins(self, plugin_dir, plugin_type: PluginType):
        load_dotenv()  # load environment variables from .env file
        envVarName = f"PODCAST_{plugin_type.value}_PLUGINS"
        allowedPlugins = os.getenv(envVarName).split(",")

        plugins = {}
        for filename in os.listdir(plugin_dir):
            if filename.endswith(".py"):
                name = filename[:-3]
                if name in allowedPlugins:
                    spec = importlib.util.spec_from_file_location(
                        name, os.path.join(plugin_dir, filename)
                    )
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
                        if not plugin.plugin.doesOutputFileExist(
                            story, storiesDirName, storyFileNameLambda
                        ):
                            plugin.plugin.writeToDisk(
                                story, storiesDirName, storyFileNameLambda
                            )
            else:
                print(f"Plugin {name} does not implement the necessary interface.")

        return stories

    def runPodcastDetailsPlugins(self, plugins, podcastName, stories):
        for name, plugin in plugins.items():
            if isinstance(plugin.plugin, BaseDataSourcePlugin):
                print(
                    f"Running Data Source Plugins again to write podcast details: {plugin.plugin.identify()}"
                )
                plugin.plugin.writePodcastDetails(f"output/{podcastName}", stories)

    def runIntroPlugins(
        self, plugins, stories, podcastName, introDirName, typeOfPodcast
    ):
        for name, plugin in plugins.items():
            if isinstance(plugin.plugin, BaseIntroPlugin):
                print(f"Running Intro Plugins: {plugin.plugin.identify()}")
                if not plugin.plugin.doesOutputFileExist(introDirName):
                    introText = plugin.plugin.writeIntro(
                        stories, podcastName, typeOfPodcast
                    )
                    plugin.plugin.writeToDisk(introText, introDirName)
            else:
                print(f"Plugin {name} does not implement the necessary interface.")

    def runStoryScraperPlugins(
        self, plugins, stories, rawTextDirName, rawTextFileNameLambda
    ):
        for name, plugin in plugins.items():
            if isinstance(plugin.plugin, BaseStoryScraperPlugin):
                print(f"Running Scraper Plugins: {plugin.plugin.identify()}")
                for story in stories:
                    if not plugin.plugin.doesHandleStory(story):
                        print(
                            f"Plugin {name} does not handle story {story['uniqueId']}"
                        )
                        continue
                    if not plugin.plugin.doesOutputFileExist(
                        story, rawTextDirName, rawTextFileNameLambda
                    ):
                        scrapedText = plugin.plugin.scrapeSiteForText(story)
                        plugin.plugin.writeToDisk(
                            story, scrapedText, rawTextDirName, rawTextFileNameLambda
                        )
            else:
                print(f"Plugin {name} does not implement the necessary interface.")

    def runStorySummarizerPlugins(
        self, plugins, stories, summaryTextDirName, summaryTextFileNameLambda
    ):
        for name, plugin in plugins.items():
            if isinstance(plugin.plugin, BaseSummaryPlugin):
                print(f"Running Summary Plugins: {plugin.plugin.identify()}")
                for story in stories:
                    if not plugin.plugin.doesOutputFileExist(
                        story, summaryTextDirName, summaryTextFileNameLambda
                    ):
                        summaryText = plugin.plugin.summarizeText(story)
                        plugin.plugin.writeToDisk(
                            story,
                            summaryText,
                            summaryTextDirName,
                            summaryTextFileNameLambda,
                        )
            else:
                print(f"Plugin {name} does not implement the necessary interface.")

    def runStorySegmentWriterPlugins(
        self, plugins, stories, segmentTextDirNameLambda, segmentTextFileNameLambda
    ):
        for name, plugin in plugins.items():
            if isinstance(plugin.plugin, BaseSegmentWriterPlugin):
                print(f"Running Segment Plugins: {plugin.plugin.identify()}")
                for story in stories:
                    if not plugin.plugin.doesOutputFileExist(
                        story, segmentTextDirNameLambda, segmentTextFileNameLambda
                    ):
                        segmentText = plugin.plugin.writeStorySegment(story, stories)
                        plugin.plugin.writeToDisk(
                            story,
                            segmentText,
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
                plugin.plugin.updateFileNames(
                    stories,
                    outroTextDirName,
                    introDirName,
                    segmentTextDirNameLambda,
                    fileNameLambda,
                )
            else:
                print(f"Plugin {name} does not implement the necessary interface.")
