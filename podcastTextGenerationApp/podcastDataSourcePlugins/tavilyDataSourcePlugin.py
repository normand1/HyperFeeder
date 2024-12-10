import os

from json_utils import dump_json
from langchain_core.tools import tool
from podcastDataSourcePlugins.baseDataSourcePlugin import BaseDataSourcePlugin
from podcastDataSourcePlugins.models.tavilyStory import TavilyStory
from services.tavily_client import CachedTavilyClient
from colorama import Fore, Style


class TavilyDataSourcePlugin(BaseDataSourcePlugin):
    @classmethod
    def identify(cls, simpleName=False) -> str:
        if simpleName:
            return "tavily"
        else:
            return "🔎 Tavily Data Source Plugin"

    @staticmethod
    @tool(name_or_callable="TavilyDataSourcePlugin-_-search")
    def search(searchQuery: str) -> list[TavilyStory]:
        """
        Tavily is a general purpose search engine like google that can be used to find articles, videos, images, and other content.
        """
        tavily_client = CachedTavilyClient()
        stories = tavily_client.search(searchQuery)
        print(f"{Fore.GREEN}{Style.BRIGHT}Fetched {len(stories)} stories from Tavily{Style.RESET_ALL}")
        # Convert to TavilyStory objects
        return [TavilyStory.from_dict(s) for s in stories]

    def writePodcastDetails(self, podcastName, stories):
        os.makedirs(podcastName, exist_ok=True)
        with open(podcastName + "/podcastDetails.json", "w", encoding="utf-8") as file:
            dump_json(stories, file)

    def filterForImportantContextOnly(self, subStoryContent: dict):
        keysToKeep = ["title", "content", "raw_content", "uniqueId"]
        return {key: subStoryContent[key] for key in keysToKeep if key in subStoryContent}

    def fetchContentForStory(self, story: TavilyStory):
        return story.content


plugin = TavilyDataSourcePlugin()
