import json
import os

from podcastScraperPlugins.abstractPluginDefinitions.abstractStoryScraperPlugin import AbstractStoryScraperPlugin
from podcastScraperPlugins.utilities.newsScraper import NewsScraper

class NewsStoryScraperPlugin(AbstractStoryScraperPlugin):

    def identify(self) -> str:
        return "NewsStoryScraperPlugin"

    def scrapeSitesForText(self, topStories, rawTextDirName, rawTextFileNameLambda):
        print("Scraping news sites for text...")
        for story in topStories:
            url = story["link"]
            rawTextFileName = rawTextFileNameLambda(story["newsRank"], url)
            filePath = os.path.join(rawTextDirName, rawTextFileName)
            if os.path.exists(filePath):
                print("raw text file already exists for url: " + url + ", skipping scraping story")
                break
            else:
                print("Scraping: " + url)
                texts = self.scrapeStoryText(url)
                
                os.makedirs(rawTextDirName, exist_ok=True)
                
                with open(filePath, 'w') as file:
                    file.write(texts)
                    file.flush()

    def scrapeStoryText(self, url):
        scraper = NewsScraper()
        try:
            article = scraper.scrape(url)
            return article
        except:
            print("Scraping failed, skipping story")
            return "This story could not be scraped. Please replace this text with any text you can find at this url: \n" + url + " \n and re-run the script."

plugin = NewsStoryScraperPlugin()