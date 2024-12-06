import requests, os, json, copy
from podcastDataSourcePlugins.baseDataSourcePlugin import BaseDataSourcePlugin
from podcastDataSourcePlugins.models.RSSItemStory import RSSItemStory
from xml.etree import ElementTree as ET


class ArticlesRSSFeedPlugin(BaseDataSourcePlugin):
    def __init__(self):
        super().__init__()
        self.feeds = []

    def identify(self) -> str:
        return "🗞️ Articles Feed API Plugin"

    def fetchStories(self):
        newsletter_rss_feeds = os.getenv("ARTICLES_RSS_FEEDS")
        number_of_items_to_fetch = os.getenv("NUMBER_OF_ITEMS_TO_FETCH")
        if not newsletter_rss_feeds:
            raise ValueError("ARTICLES_RSS_FEEDS environment variable is not set, please set it and try again.")

        self.feeds = newsletter_rss_feeds.split(",")
        print(self.feeds)
        if not self.feeds:
            raise ValueError("No articles RSS feeds in .config.env file, please add one and try again.")
        stories = []
        for feed_url in self.feeds:
            response = requests.get(feed_url)
            root = ET.fromstring(response.content)
            for index, item in enumerate(root.findall(".//item")[:number_of_items_to_fetch]):
                # serialize the item to a string
                item_xml = ET.tostring(item, encoding="utf8").decode("utf8")
                story = RSSItemStory(
                    itemOrder=index,
                    title=item.find("title").text or root.find(".//channel/title").text,
                    link=item.find("link").text,
                    storyType="Article",
                    source="RSS Feed",
                    rssItem=item_xml,
                    uniqueId=self.url_to_filename(item.find("guid").text),
                    rootLink=feed_url,
                    pubDate=(item.find("pubDate").text if item.find("pubDate") is not None else None),
                    newsRank=index,
                )
                stories.append(story.to_dict())
        return stories

    def writePodcastDetails(self, podcastName, stories):
        os.makedirs(podcastName, exist_ok=True)
        with open(podcastName + "/podcastDetails.json", "w") as file:
            json.dump(stories, file)

    def writeToDisk(self, story, storiesDirName, storyFileNameLambda):
        url = story.link
        uniqueId = story.uniqueId
        rawTextFileName = storyFileNameLambda(uniqueId, url)
        filePath = os.path.join(storiesDirName, rawTextFileName)
        os.makedirs(storiesDirName, exist_ok=True)
        with open(filePath, "w") as file:
            json.dump(story, file)
            file.flush()


plugin = ArticlesRSSFeedPlugin()
