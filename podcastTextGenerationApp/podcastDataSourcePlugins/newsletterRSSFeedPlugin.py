import json
import os
import re
from datetime import datetime
from urllib.parse import urlparse
from xml.etree import ElementTree as ET
from dateutil.parser import parse
import firebase_admin
from firebase_admin import credentials, db

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
        # pylint: disable=import-outside-toplevel
        newsletterRSSFeed = os.getenv("NEWSLETTER_RSS_FEEDS")
        firebaseServiceAccountKeyPath = os.getenv("FIREBASE_SERVICE_ACCOUNT_KEY_PATH")
        lastFetched = None
        if not newsletterRSSFeed:
            raise ValueError(
                "NEWSLETTER_RSS_FEEDS environment variable is not set, please set it and try again."
            )
        self.setupFirebaseIfNeeded(firebaseServiceAccountKeyPath)

        self.feeds = newsletterRSSFeed.split(",")
        numberOfItemsToFetch = int(os.getenv("NUMBER_OF_ITEMS_TO_FETCH"))
        if not numberOfItemsToFetch:
            raise ValueError(
                "NUMBER_OF_ITEMS_TO_FETCH environment variable is not set, please set it and try again."
            )

        if not self.feeds:
            raise ValueError(
                "No podcast feeds in .env file, please add one and try again."
            )
        stories = []
        for feedUrl in self.feeds:
            response = requests.get(feedUrl, timeout=10)
            root = ET.fromstring(response.content)
            rootLink = root.find(".//channel/link").text
            parsedUrl = urlparse(rootLink)
            cleanLink = parsedUrl.netloc + parsedUrl.path
            cleanLink = re.sub(r"\W+", "", cleanLink)

            if firebaseServiceAccountKeyPath:
                ref = db.reference(f"newsletter/{cleanLink}/")
                lastFetched = ref.get()
                if lastFetched:
                    lastFetched = parse(lastFetched["lastFetched"])
            self.getStoriesFromFeed(
                lastFetched, numberOfItemsToFetch, stories, root, cleanLink
            )
        if len(stories) > 0:
            # Sort the stories by publication date in descending order
            stories.sort(key=lambda x: x["pubDate"], reverse=True)
            mostRecentStory = stories[0]
            mostRecentTimestamp = mostRecentStory["pubDate"]
            ref.set({"lastFetched": mostRecentTimestamp})
            return stories
        return []

    def getStoriesFromFeed(
        self, lastFetched, numberOfItemsToFetch, stories, root, cleanLink
    ):
        for index, item in enumerate(root.findall(".//item")[:numberOfItemsToFetch]):
            # serialize the item to a string
            itemXml = ET.tostring(item, encoding="utf8").decode("utf8")
            itemGuid = item.find("guid").text
            pubDateString = item.find("pubDate").text
            pubDate = datetime.strptime(pubDateString, "%a, %d %b %Y %H:%M:%S %Z")
            pubDate = pubDate.replace(tzinfo=pytz.UTC)
            story = RSSItemStory(
                itemOrder=index,
                title=itemGuid,
                link=itemGuid,
                storyType=root.find(".//channel/title").text,
                source="RSS Feed",
                rssItem=itemXml,
                uniqueId=self.url_to_filename(itemGuid),
                rootLink=cleanLink,
                pubDate=pubDate.isoformat(),
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

    def setupFirebaseIfNeeded(self, firebaseServiceAccountKeyPath):
        if firebaseServiceAccountKeyPath:
            if os.getenv("FIREBASE_DATABASE_URL") is None:
                raise ValueError(
                    "FIREBASE_DATABASE_URL environment variable is not set, please set it in .env and try again."
                )
            cred = credentials.Certificate(firebaseServiceAccountKeyPath)
            firebase_admin.initialize_app(
                cred,
                {"databaseURL": os.getenv("FIREBASE_DATABASE_URL")},
            )


plugin = NewsletterRSSFeedPlugin()
