from podcastScraperPlugins.baseStoryScraperPlugin import BaseStoryScraperPlugin
from podcastScraperPlugins.utilities.newsScraper import NewsScraper
from podcastSegmentWriterPlugins.utilities.utils import storyCouldNotBeScrapedText


class NewsStoryScraperPlugin(BaseStoryScraperPlugin):
    def identify(self) -> str:
        return "📰 NewsStoryScraperPlugin"

    def doesHandleStory(self, story) -> bool:
        return getattr(story, "storyType", False) in ["Article", "Newsletter"]

    def scrapeSiteForText(self, story, storiesDirName) -> str:
        if "link" not in story:
            return ""
        url = story.link
        print("Scraping: " + url)
        texts = self.scrapeStoryText(url)
        return texts

    def scrapeStoryText(self, url):
        scraper = NewsScraper()
        try:
            article = scraper.scrape(url)
            return article
        except Exception as e:
            print(f"Scraping failed, skipping story: {str(e)}")
            return f"{storyCouldNotBeScrapedText()}\n{url}"

    def scrapeResearchAndOrganizeForSegmentWriter(self, story, storiesDirName) -> str:
        return ""


plugin = NewsStoryScraperPlugin()
