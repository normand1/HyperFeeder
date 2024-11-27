import json
import os

from podcastScraperPlugins.baseStoryScraperPlugin import BaseStoryScraperPlugin
from podcastScraperPlugins.utilities.newsScraper import NewsScraper


class TesterScraperPlugin(BaseStoryScraperPlugin):
    def identify(self) -> str:
        return "📰🧪 NewsStoryScraperPlugin"

    def doesHandleStory(self, story) -> bool:
        return True

    def scrapeSiteForText(self, story, storiesDirName) -> str:
        assert story is not None
        assert story["link"] is not None
        texts = self.scrapeStoryText(story["link"])
        return texts

    def scrapeStoryText(self, url):
        assert url is not None
        return "test scraped story text"


plugin = TesterScraperPlugin()
