import requests
from podcastScraperPlugins.baseStoryScraperPlugin import BaseStoryScraperPlugin


class RawScraperPlugin(BaseStoryScraperPlugin):
    def identify(self) -> str:
        return "🍣 RawScraperPlugin"

    def doesHandleStory(self, story) -> bool:
        return "link" in story and "rssItem" not in story

    def scrapeSiteForText(self, story) -> str:
        url = story["link"]
        rawTextFromUrlResponse = requests.get(url, timeout=10)
        return rawTextFromUrlResponse.text


plugin = RawScraperPlugin()
