import os
import importlib.util
from podcastDataSourcePlugins.abstractPluginDefinitions.abstractDataSourcePlugin import AbstractDataSourcePlugin
from podcastIntroPlugins.abstractPluginDefinitions.abstractIntroPlugin import AbstractIntroPlugin
from podcastScraperPlugins.abstractPluginDefinitions.abstractStoryScraperPlugin import AbstractStoryScraperPlugin
from podcastSummaryPlugins.abstractPluginDefinitions.abstractStorySummaryPlugin import AbstractStorySummaryPlugin
from podcastSegmentWriterPlugins.abstractPluginDefinitions.abstractSegmentWriterPlugin import AbstractSegmentWriterPlugin
from dotenv import load_dotenv
from pluginTypes import PluginType

class PluginManager:
    def load_plugins(self, plugin_dir, plugin_type: PluginType):
        load_dotenv()  # load environment variables from .env file
        env_var_name = f"PODCAST_{plugin_type.value}_PLUGINS"
        allowed_plugins = os.getenv(env_var_name).split(',')

        plugins = {}
        for filename in os.listdir(plugin_dir):
            if filename.endswith('.py'):
                name = filename[:-3]
                if name in allowed_plugins:
                    spec = importlib.util.spec_from_file_location(name, os.path.join(plugin_dir, filename))
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    plugins[name] = module
        return plugins
    
    def runDataSourcePlugins(self, plugins, podcastName):
        results = []
        for name, plugin in plugins.items():
            if isinstance(plugin.plugin, AbstractDataSourcePlugin):
                print(f"Running Data Source Plugin: {plugin.plugin.identify()}")
                fetchedStory = plugin.plugin.fetchStories()
                
                if fetchedStory is not None:
                    results.extend(fetchedStory) 
            else:
                print(f"Plugin {name} does not implement the necessary interface.")
        plugin.plugin.writePodcastDetails(podcastName, results)
        return results
    
    def runIntroPlugins(self, plugins, topStories, podcastName, fileNameIntro, typeOfPodcast):
        for name, plugin in plugins.items():
            if isinstance(plugin.plugin, AbstractIntroPlugin):
                print(f"Running Intro Plugin: {plugin.plugin.identify()}")
                plugin.plugin.writeIntro(topStories, podcastName, fileNameIntro, typeOfPodcast)
            else:
                print(f"Plugin {name} does not implement the necessary interface.")
    
    def runStoryScraperPlugins(self, plugins, topStories, rawTextDirName, rawTextFileNameLambda):
        for name, plugin in plugins.items():
            if isinstance(plugin.plugin, AbstractStoryScraperPlugin):
                print(f"Running Intro Plugin: {plugin.plugin.identify()}")
                plugin.plugin.scrapeSitesForText(topStories, rawTextDirName, rawTextFileNameLambda)
            else:
                print(f"Plugin {name} does not implement the necessary interface.")
    
    def runStorySummarizerPlugins(self, plugins, topStories, summaryTextDirNameLambda, summaryTextFileNameLambda):
        for name, plugin in plugins.items():
            if isinstance(plugin.plugin, AbstractStorySummaryPlugin):
                print(f"Running Intro Plugin: {plugin.plugin.identify()}")
                plugin.plugin.summarizeText(topStories, summaryTextDirNameLambda, summaryTextFileNameLambda)
            else:
                print(f"Plugin {name} does not implement the necessary interface.")
    
    def runStorySegmentWriterPlugins(self, plugins, topStories, segmentTextDirNameLambda, segmentTextFileNameLambda):
        for name, plugin in plugins.items():
            if isinstance(plugin.plugin, AbstractSegmentWriterPlugin):
                print(f"Running Intro Plugin: {plugin.plugin.identify()}")
                plugin.plugin.writeStorySegment(topStories, segmentTextDirNameLambda, segmentTextFileNameLambda)
            else:
                print(f"Plugin {name} does not implement the necessary interface.")