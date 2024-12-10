import requests
from podcastScraperPlugins.baseStoryScraperPlugin import BaseStoryScraperPlugin
from podcastSegmentWriterPlugins.utilities.utils import storyCouldNotBeScrapedText


class RawScraperPlugin(BaseStoryScraperPlugin):
    def identify(self) -> str:
        return "🍣 RawScraperPlugin"

    def doesHandleStory(self, story) -> bool:
        return "link" in story and "rssItem" not in story

    def scrapeSiteForText(self, story, storiesDirName=None) -> str:
        try:
            url = story.link
            rawTextFromUrlResponse = requests.get(url, timeout=10)
            return rawTextFromUrlResponse.text
        except Exception as e:
            print(f"Error scraping site for text: {e}")
            return storyCouldNotBeScrapedText()


plugin = RawScraperPlugin()
