import xml.etree.ElementTree as ET

from podcastScraperPlugins.baseStoryScraperPlugin import BaseStoryScraperPlugin


class RSSItemScraperPlugin(BaseStoryScraperPlugin):
    def identify(self) -> str:
        return "🛜 RSSItemScraperPlugin"

    def doesHandleStory(self, story) -> bool:
        return getattr(story, "rssItem", False)

    def scrapeSiteForText(self, story, storiesDirName) -> str:
        if not getattr(story, "rssItem", False):
            return ""
        rssItem = story.rssItem
        root = ET.fromstring(rssItem)
        namespaces = {"content": "http://purl.org/rss/1.0/modules/content/"}
        content = root.find("content:encoded", namespaces).text
        return content


plugin = RSSItemScraperPlugin()
