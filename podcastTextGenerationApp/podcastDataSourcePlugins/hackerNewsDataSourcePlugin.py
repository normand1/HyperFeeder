import json
import os

import requests
from podcastDataSourcePlugins.baseDataSourcePlugin import BaseDataSourcePlugin
from podcastDataSourcePlugins.models.hackerNewsStory import HackerNewsStory
from langchain_core.tools import tool
from podcastScraperPlugins.newsStoryScraperPlugin import NewsStoryScraperPlugin
from colorama import Fore, Style


class HackerNewsDataSourcePlugin(BaseDataSourcePlugin):
    def __init__(self):
        super().__init__()
        self.scraperPlugin = NewsStoryScraperPlugin()

    @classmethod
    def identify(cls, simpleName=False) -> str:
        if simpleName:
            return "hackerNews"
        else:
            return "🧑‍💻 Hacker News API Plugin"

    @staticmethod
    @tool(name_or_callable="HackerNewsDataSourcePlugin-_-searchTopStories")
    def searchTopStories(topStoriesCount: int = 5):
        """
        Search for the top segments on Hacker News
        """
        baseUrl = "https://hacker-news.firebaseio.com/v0/"

        topStoriesUrl = f"{baseUrl}topstories.json"
        response = requests.get(topStoriesUrl, timeout=10)
        topStoriesIds = response.json()

        segments = []

        for rank, storyId in enumerate(topStoriesIds[:topStoriesCount]):
            storyUrl = f"{baseUrl}item/{storyId}.json"
            response = requests.get(storyUrl, timeout=10)
            storyData = response.json()

            story = HackerNewsStory(
                newsRank=rank,
                title=storyData.get("title"),
                link=storyData.get("url"),
                content="",  # fetchContentForStory will add content
                raw_content="",  # fetchContentForStory will add raw_content
                uniqueId=HackerNewsDataSourcePlugin.makeUniqueStoryIdentifier(),
            )
            segments.append(story)
        print(f"{Fore.GREEN}{Style.BRIGHT}Fetched {len(segments)} segments from Hacker News{Style.RESET_ALL}")
        return segments

    def writePodcastDetails(self, podcastName, segments):
        os.makedirs(podcastName, exist_ok=True)
        with open(podcastName + "/podcastDetails.json", "w", encoding="utf-8") as file:
            json.dump(segments, file)

    def filterForImportantContextOnly(self, subStoryContent: dict):
        keysToKeep = ["title", "content"]
        return {key: subStoryContent[key] for key in keysToKeep if key in subStoryContent}

    def fetchContentForStory(self, story: HackerNewsStory):
        return self.scraperPlugin.scrapeStoryText(story.link)


plugin = HackerNewsDataSourcePlugin()
