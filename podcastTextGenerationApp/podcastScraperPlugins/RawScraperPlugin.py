from podcastScraperPlugins.baseStoryScraperPlugin import BaseStoryScraperPlugin
import requests
import os


class RawScraperPlugin(BaseStoryScraperPlugin):
    def identify(self) -> str:
        return "RawScraperPlugin"

    def scrapeSiteForText(self, story) -> str:
        url = story["link"]
        raw_text_from_url_response = requests.get(url)
        return raw_text_from_url_response.text


plugin = RawScraperPlugin()
