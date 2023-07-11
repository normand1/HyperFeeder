import json
import os

from podcastScraperPlugins.baseStoryScraperPlugin import BaseStoryScraperPlugin
from podcastScraperPlugins.utilities.newsScraper import NewsScraper


class NewsStoryScraperPlugin(BaseStoryScraperPlugin):
    def identify(self) -> str:
        return "📰 NewsStoryScraperPlugin"

    def scrapeSiteForText(self, story) -> str:
        url = story["link"]
        print("Scraping: " + url)
        texts = self.scrapeStoryText(url)
        return texts

    def scrapeStoryText(self, url):
        scraper = NewsScraper()
        try:
            article = scraper.scrape(url)
            return article
        except:
            print("Scraping failed, skipping story")
            return (
                "This story could not be scraped. Please replace this text with any text you can find at this url: \n"
                + url
                + " \n and re-run the script."
            )


plugin = NewsStoryScraperPlugin()
