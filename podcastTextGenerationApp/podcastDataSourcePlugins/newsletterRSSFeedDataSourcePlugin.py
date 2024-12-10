import json
import os
import re
from datetime import datetime
from urllib.parse import urlparse
from xml.etree import ElementTree as ET

import pytz
import requests
from podcastDataSourcePlugins.baseDataSourcePlugin import BaseDataSourcePlugin
from podcastDataSourcePlugins.models.RSSItemStory import RSSItemStory
from SQLiteManager import SQLiteManager
from langchain_core.tools import tool
from podcastScraperPlugins.newsStoryScraperPlugin import NewsStoryScraperPlugin
from colorama import Fore, Style


class RSSFeedDataSourcePlugin(BaseDataSourcePlugin):
    def __init__(self):
        super().__init__()
        self.scraperPlugin = NewsStoryScraperPlugin()

    @classmethod
    def identify(cls, simpleName=False) -> str:
        if simpleName:
            return "newsletterRSSFeed"
        else:
            return "🗞️ Newsletter Feed API Plugin"

    @staticmethod
    @tool(name_or_callable="RSSFeedDataSourcePlugin-_-fetchNewsletterRSSFeedStories")
    def fetchNewsletterRSSFeedStories(newsletterRssFeeds: list[str]) -> list[RSSItemStory]:
        """
        Fetch the top segments from a list of newsletter RSS feeds
        """
        sqlLiteManager = SQLiteManager()
        numberOfItemsToFetch = int(os.getenv("NEWSLETTER_RSS_NUMBER_OF_ITEMS_TO_FETCH"))
        if not numberOfItemsToFetch:
            raise ValueError("NEWSLETTER_RSS_NUMBER_OF_ITEMS_TO_FETCH environment variable is not set, please set it and try again.")

        if not newsletterRssFeeds:
            raise ValueError("No newsletter RSS feeds in prompt, please add one and try again.")
        segments = []
        # Iterate through each Newsletter Feed
        for feedUrl in newsletterRssFeeds:
            response = requests.get(feedUrl, timeout=10)
            root = ET.fromstring(response.content)
            rootLink = root.find(".//channel/link").text
            parsedUrl = urlparse(rootLink)
            cleanLink = parsedUrl.netloc + parsedUrl.path
            cleanLink = re.sub(r"\W+", "", cleanLink)
            # TODO: Fix this
            # lastFetched = sqlLiteManager.get_last_fetched(cleanLink)

            # Iterate through each newsletter item
            RSSFeedDataSourcePlugin.getStoriesFromFeed(None, numberOfItemsToFetch, segments, root, feedUrl)
        if len(segments) > 0:
            # Sort the segments by publication date in descending order
            segments.sort(key=lambda x: x.pubDate, reverse=True)
            mostRecentStory = segments[0]
            mostRecentTimestamp = mostRecentStory.pubDate
            # ref.set({"lastFetched": mostRecentTimestamp})
            sqlLiteManager.set_last_fetched(cleanLink, mostRecentTimestamp)
            print(f"{Fore.GREEN}{Style.BRIGHT}Fetched {len(segments)} segments from Newsletter RSS Feed{Style.RESET_ALL}")
            return segments
        print(f"{Fore.RED}{Style.BRIGHT}No segments found in Newsletter RSS Feed{Style.RESET_ALL}")
        return []

    @staticmethod
    def getStoriesFromFeed(lastFetched: datetime, numberOfItemsToFetch: int, segments: list[RSSItemStory], root: ET.Element, cleanLink: str):
        for index, item in enumerate(root.findall(".//item")[:numberOfItemsToFetch]):
            # serialize the item to a string
            itemXml = ET.tostring(item, encoding="utf8").decode("utf8")
            itemGuid = item.find("guid").text
            itemLink = item.find("link").text
            pubDateString = item.find("pubDate").text
            pubDate = BaseDataSourcePlugin.parseDate(pubDateString)
            pubDate = pubDate.replace(tzinfo=pytz.UTC)
            story = RSSItemStory(
                itemOrder=index,
                title=root.find(".//channel/title").text or itemGuid,
                link=itemLink,
                content="",  # Will be filled by fetchContentForStory
                raw_content="",  # Will be filled by fetchContentForStory
                rssItem=itemXml,
                uniqueId=BaseDataSourcePlugin.url_to_filename(itemGuid),
                rootLink=cleanLink,
                pubDate=pubDate.isoformat(),
                newsRank=index,
            )

            if (lastFetched and pubDate > lastFetched) or not lastFetched:
                segments.append(story)

    def writePodcastDetails(self, podcastName, segments):
        os.makedirs(podcastName, exist_ok=True)
        with open(podcastName + "/podcastDetails.json", "w", encoding="utf-8") as file:
            json.dump(segments, file)

    @staticmethod
    def writeToDisk(story, storiesDirName, storyFileNameLambda):
        url = story.link
        uniqueId = story.uniqueId
        rawTextFileName = storyFileNameLambda(uniqueId, url)
        filePath = os.path.join(storiesDirName, rawTextFileName)
        os.makedirs(storiesDirName, exist_ok=True)
        with open(filePath, "w", encoding="utf-8") as file:
            json.dump(story, file)
            file.flush()

    def fetchContentForStory(self, story: RSSItemStory):
        return self.scraperPlugin.scrapeStoryText(story.link)

    def filterForImportantContextOnly(self, subStoryContent: dict):
        keysToKeep = ["title", "content", "raw_content", "uniqueId"]
        return {key: subStoryContent[key] for key in keysToKeep if key in subStoryContent}


plugin = RSSFeedDataSourcePlugin()
