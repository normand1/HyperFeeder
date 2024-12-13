import feedparser
import os
import json
from datetime import datetime, timedelta
from podcastDataSourcePlugins.baseDataSourcePlugin import BaseDataSourcePlugin
from podcastDataSourcePlugins.models.arxivPaperStory import (
    ArxivPaperStory,
)
from podcastScraperPlugins.newsStoryScraperPlugin import NewsStoryScraperPlugin
from langchain_core.tools import tool
from colorama import Fore, Style


class ArxivDataSourcePlugin(BaseDataSourcePlugin):
    def __init__(self):
        super().__init__()
        self.scraperPlugin = NewsStoryScraperPlugin()

    @classmethod
    def identify(cls, simpleName=False) -> str:
        if simpleName:
            return "arxiv"
        else:
            return "📖 ArXiv API Plugin"

    @staticmethod
    @tool(name_or_callable="ArxivDataSourcePlugin-_-searchForPapers")
    def searchForPapers(searchQuery: str = None):
        """
        Search for papers on ArXiv from the past week
        """
        oneWeekAgo = datetime.now() - timedelta(weeks=1)
        feed = feedparser.parse(f"https://export.arxiv.org/api/query?search_query=all:{searchQuery}&sortBy=submittedDate&sortOrder=descending&start=0&max_results=2".format())

        # Filter for entries from the past week and format them
        recentPapers = [
            ArxivPaperStory(
                newsRank=index,
                title=entry.title,
                link=entry.link,
                content="",  # fetchContentForStory will add content
                raw_content="",  # fetchContentForStory will add raw_content
                uniqueId=ArxivDataSourcePlugin.makeUniqueStoryIdentifier(),
            )
            for index, entry in enumerate(feed.entries)
            if datetime(*entry.published_parsed[:6]) > oneWeekAgo
        ]
        print(f"{Fore.GREEN}{Style.BRIGHT}Fetched {len(recentPapers)} segments from ArXiv{Style.RESET_ALL}")
        return recentPapers

    def writePodcastDetails(self, podcastName, segments):
        os.makedirs(podcastName, exist_ok=True)
        with open(podcastName + "/podcastDetails.json", "w", encoding="utf-8") as file:
            json.dump(segments, file)

    def fetchContentForStory(self, story: ArxivPaperStory):
        return self.scraperPlugin.scrapeStoryText(story.link)

    def filterForImportantContextOnly(self, subStoryContent: dict):
        keysToKeep = ["title", "content", "raw_content", "uniqueId"]
        return {key: subStoryContent[key] for key in keysToKeep if key in subStoryContent}


plugin = ArxivDataSourcePlugin()
