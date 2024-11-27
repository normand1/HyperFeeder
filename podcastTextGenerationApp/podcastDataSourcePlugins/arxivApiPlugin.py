import feedparser
import os
import json
from datetime import datetime, timedelta
from podcastDataSourcePlugins.baseDataSourcePlugin import BaseDataSourcePlugin
from podcastDataSourcePlugins.models.arxivPaperStory import (
    ArxivPaperStory,
)  # Assuming this model can be reused, otherwise, create a new one
from urllib.parse import quote


class ArxivAPIPlugin(BaseDataSourcePlugin):
    def __init__(self):
        super().__init__()

    def identify(self) -> str:
        return "📖 ArXiv API Plugin"

    def fetchStories(self):
        # Define the date one week ago
        one_week_ago = datetime.now() - timedelta(weeks=1)
        search_query = quote(os.getenv("ARXIV_SEARCH_QUERY"))
        # Fetch recent AI papers
        feed = feedparser.parse(
            f"https://export.arxiv.org/api/query?search_query=all:{search_query}&sortBy=submittedDate&sortOrder=descending&start=0&max_results=100".format()
        )

        # Filter for entries from the past week and format them
        recent_papers = [
            ArxivPaperStory(
                newsRank=index,
                title=entry.title,
                link=entry.link,
                storyType="paper",  # Or any other appropriate type you'd like
                uniqueId=self.makeUniqueStoryIdentifier(),
            ).to_dict()
            for index, entry in enumerate(feed.entries)
            if datetime(*entry.published_parsed[:6]) > one_week_ago
        ]

        return recent_papers

    def writePodcastDetails(self, podcastName, stories):
        os.makedirs(podcastName, exist_ok=True)
        with open(podcastName + "/podcastDetails.json", "w", encoding="utf-8") as file:
            json.dump(stories, file)


plugin = ArxivAPIPlugin()
