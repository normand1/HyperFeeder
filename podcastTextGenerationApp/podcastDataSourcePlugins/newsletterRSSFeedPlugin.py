import requests, os, json, copy
from podcastDataSourcePlugins.baseDataSourcePlugin import BaseDataSourcePlugin
from podcastDataSourcePlugins.models.RSSItemStory import RSSItemStory
from xml.etree import ElementTree as ET


class NewsletterRSSFeedPlugin(BaseDataSourcePlugin):
    def __init__(self):
        super().__init__()
        self.feeds = []

    def identify(self) -> str:
        return "🗞️ Newsletter Feed API Plugin"

    def fetchStories(self):
        newsletter_rss_feeds = os.getenv("NEWSLETTER_RSS_FEEDS")
        if not newsletter_rss_feeds:
            raise ValueError(
                "NEWSLETTER_RSS_FEEDS environment variable is not set, please set it and try again."
            )

        self.feeds = newsletter_rss_feeds.split(",")

        if not self.feeds:
            raise ValueError(
                "No podcast feeds in .env file, please add one and try again."
            )
        stories = []
        for feed_url in self.feeds:
            response = requests.get(feed_url)
            root = ET.fromstring(response.content)
            for index, item in enumerate(root.findall(".//item")[:5]):
                # serialize the item to a string
                item_xml = ET.tostring(item, encoding="utf8").decode("utf8")
                story = RSSItemStory(
                    itemOrder=index,
                    title=item.find("title").text,
                    link=item.find("guid").text,
                    storyType=root.find(".//channel/title").text,
                    source="RSS Feed",
                    rssItem=item_xml,
                    uniqueId=self.url_to_filename(item.find("guid").text),
                )
                stories.append(story.to_dict())
        return stories

    def writePodcastDetails(self, podcastName, stories):
        os.makedirs(podcastName, exist_ok=True)
        with open(podcastName + "/podcastDetails.json", "w") as file:
            json.dump(stories, file)

    def writeToDisk(self, story, storiesDirName, storyFileNameLambda):
        url = story["link"]
        uniqueId = story["uniqueId"]
        rawTextFileName = storyFileNameLambda(uniqueId, url)
        filePath = os.path.join(storiesDirName, rawTextFileName)
        os.makedirs(storiesDirName, exist_ok=True)
        with open(filePath, "w") as file:
            json.dump(story, file)
            file.flush()


plugin = NewsletterRSSFeedPlugin()
