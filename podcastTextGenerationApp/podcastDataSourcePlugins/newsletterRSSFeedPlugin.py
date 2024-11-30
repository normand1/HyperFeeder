import json
import os
import re
from urllib.parse import urlparse
from xml.etree import ElementTree as ET
from dateutil.parser import parse
# from firebase_admin import db

import pytz
import requests
from podcastDataSourcePlugins.baseDataSourcePlugin import BaseDataSourcePlugin
from podcastDataSourcePlugins.models.RSSItemStory import RSSItemStory


class NewsletterRSSFeedPlugin(BaseDataSourcePlugin):
    def __init__(self):
        super().__init__()
        self.feeds = []

    def identify(self) -> str:
        return "🗞️ Newsletter Feed API Plugin"

    def fetchStories(self):
        newsletter_rss_feeds = os.getenv("NEWSLETTER_RSS_FEEDS")
        print(newsletter_rss_feeds + " is the value of NEWSLETTER_RSS_FEEDS")
        if not newsletter_rss_feeds:
            raise ValueError("NEWSLETTER_RSS_FEEDS environment variable is not set, please set it and try again.")

        self.feeds = newsletter_rss_feeds.split(",")
        numberOfItemsToFetch = int(os.getenv("NUMBER_OF_ITEMS_TO_FETCH"))
        if not numberOfItemsToFetch:
            raise ValueError("NUMBER_OF_ITEMS_TO_FETCH environment variable is not set, please set it and try again.")

        if not self.feeds:
            raise ValueError("No podcast feeds in .config.env file, please add one and try again.")
        stories = []
        # Iterate through each Newsletter Feed
        for feedUrl in self.feeds:
            response = requests.get(feedUrl, timeout=10)
            root = ET.fromstring(response.content)
            rootLink = root.find(".//channel/link").text
            parsedUrl = urlparse(rootLink)
            cleanLink = parsedUrl.netloc + parsedUrl.path
            cleanLink = re.sub(r"\W+", "", cleanLink)
            lastFetched = self.sqlite_manager.get_last_fetched(cleanLink)

            # if self.firebaseServiceAccountKeyPath:
            #     ref = db.reference(f"newsletter/{cleanLink}/")
            #     lastFetched = ref.get()
            #     if lastFetched:
            #         lastFetched = parse(lastFetched["lastFetched"])


            # Iterate through each newsletter item
            self.getStoriesFromFeed(lastFetched, numberOfItemsToFetch, stories, root, cleanLink)
        if len(stories) > 0:
            # Sort the stories by publication date in descending order
            stories.sort(key=lambda x: x["pubDate"], reverse=True)
            mostRecentStory = stories[0]
            mostRecentTimestamp = mostRecentStory["pubDate"]
            # ref.set({"lastFetched": mostRecentTimestamp})
            self.sqlite_manager.set_last_fetched(cleanLink, mostRecentTimestamp)

            return stories
        return []

    def getStoriesFromFeed(self, lastFetched, numberOfItemsToFetch, stories, root, cleanLink):
        for index, item in enumerate(root.findall(".//item")[:numberOfItemsToFetch]):
            # serialize the item to a string
            itemXml = ET.tostring(item, encoding="utf8").decode("utf8")
            itemGuid = item.find("guid").text
            pubDateString = item.find("pubDate").text
            pubDate = self.parseDate(pubDateString)
            pubDate = pubDate.replace(tzinfo=pytz.UTC)
            story = RSSItemStory(
                itemOrder=index,
                title=root.find(".//channel/title").text or itemGuid,
                link=itemGuid,
                storyType="Newsletter",
                source="RSS Feed",
                rssItem=itemXml,
                uniqueId=self.url_to_filename(itemGuid),
                rootLink=cleanLink,
                pubDate=pubDate.isoformat(),
                newsRank=index,
            )
            # If you've provided the firebaseServiceAccountKeyPath then we'll use firebase to store the lastFetched date
            # otherwise we'll return the <NUMBER_OF_ITEMS_TO_FETCH> most recent stories in the feed
            if (lastFetched and pubDate > lastFetched) or not lastFetched:
                stories.append(story.to_dict())

    def writePodcastDetails(self, podcastName, stories):
        os.makedirs(podcastName, exist_ok=True)
        with open(podcastName + "/podcastDetails.json", "w", encoding="utf-8") as file:
            json.dump(stories, file)

    def writeToDisk(self, story, storiesDirName, storyFileNameLambda):
        url = story["link"]
        uniqueId = story["uniqueId"]
        rawTextFileName = storyFileNameLambda(uniqueId, url)
        filePath = os.path.join(storiesDirName, rawTextFileName)
        os.makedirs(storiesDirName, exist_ok=True)
        with open(filePath, "w", encoding="utf-8") as file:
            json.dump(story, file)
            file.flush()


plugin = NewsletterRSSFeedPlugin()
