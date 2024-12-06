from podcastScraperPlugins.baseStoryScraperPlugin import BaseStoryScraperPlugin
from podcastScraperPlugins.utilities.newsScraper import NewsScraper
from podcastSegmentWriterPlugins.utilities.utils import storyCouldNotBeScrapedText
import yaml


class TokenResearchScraperPlugin(BaseStoryScraperPlugin):
    def identify(self) -> str:
        return "🗝️ TokenResearchScraperPlugin"

    def doesHandleStory(self, story) -> bool:
        return getattr(story, "storyType", False) in ["Token"]

    def scrapeSiteForText(self, story, storiesDirName) -> str:
        return None

    def scrapeStoryText(self, url):
        return None

    def scrapeResearchAndOrganizeForSegmentWriter(self, story, storiesDirName, researchDirectoryName):
        research = self.readResearchFromDisk(story, researchDirectoryName)
        return yaml.dump(research)

    def __scrapeSiteForText(self, story, scrapeUrlKey, storiesDirName) -> str:
        if not hasattr(story, scrapeUrlKey):
            raise KeyError(f"Scrape URL key {scrapeUrlKey} not found in story")
        url = getattr(story, scrapeUrlKey)
        print("Scraping: " + url)
        texts = self.__scrapeStoryText(url)
        return texts

    def __scrapeStoryText(self, url):
        scraper = NewsScraper()
        try:
            article = scraper.scrape(url)
            return article
        except Exception as e:
            print(f"Scraping failed, skipping story: {str(e)}")
            return f"{storyCouldNotBeScrapedText()}\n{url}"


plugin = TokenResearchScraperPlugin()
