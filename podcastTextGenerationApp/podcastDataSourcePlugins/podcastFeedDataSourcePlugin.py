import copy
import json
import os
import re
from datetime import datetime
from urllib.parse import urlparse
from xml.etree import ElementTree as ET
import pytz
import requests
from podcastDataSourcePlugins.baseDataSourcePlugin import BaseDataSourcePlugin
from podcastDataSourcePlugins.models.podcastStory import PodcastStory
from langchain_core.tools import tool
from SQLiteManager import SQLiteManager


class PodcastFeedDataSourcePlugin(BaseDataSourcePlugin):
    @classmethod
    def identify(cls, simpleName=False) -> str:
        if simpleName:
            return "podcastFeed"
        else:
            return "🎙️ Podcast Transcript API Plugin"

    @staticmethod
    @tool(name_or_callable="PodcastFeedDataSourcePlugin-_-fetchPodcastFeeds")
    def fetchPodcastFeeds(podcastFeeds: list[str] = None, numberOfItemsToFetch: int = None):
        """
        Fetch the top segments from a list of podcast feeds
        """
        sqlLiteManager = SQLiteManager()
        lastFetched = None

        if not podcastFeeds:
            raise ValueError("No podcast feeds passed as argument, please add one and try again.")

        if not numberOfItemsToFetch:
            raise ValueError("NUMBER_OF_ITEMS_TO_FETCH environment variable is not set, please set it and try again.")
        segments = []
        # Iterate through each Podcast Feed
        for feedUrl in podcastFeeds:
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
            response = requests.get(feedUrl, headers=headers, timeout=10)
            root = ET.fromstring(response.content)
            rootLink = root.find(".//channel/link").text
            parsedUrl = urlparse(rootLink)
            cleanLink = parsedUrl.netloc + parsedUrl.path
            cleanLink = re.sub(r"\W+", "", cleanLink)
            lastFetched = sqlLiteManager.get_last_fetched(cleanLink)

            podcastTitle = root.find(".//channel/title")
            # Iterate through each podcast episode
            PodcastFeedDataSourcePlugin.getStoriesFromFeed(
                lastFetched,
                numberOfItemsToFetch,
                segments,
                root,
                podcastTitle,
                cleanLink,
            )
        if len(segments) > 0:
            # Sort the segments by publication date in descending order
            segments.sort(key=lambda x: x["pubDate"], reverse=True)
            mostRecentStories = segments[0:numberOfItemsToFetch]
            mostRecentTimestamp = max(story.pubDate for story in mostRecentStories)
            sqlLiteManager.set_last_fetched(cleanLink, mostRecentTimestamp)
            return mostRecentStories
        return []

    @staticmethod
    def getStoriesFromFeed(
        lastFetched,
        numberOfItemsToFetch,
        segments: list,
        root,
        podcastTitle,
        cleanLink,
    ):
        def find_element(item, tags):
            for tag in tags:
                element = item.find(f".//{tag}")
                if element is not None:
                    return element
            return None

        items = root.findall(".//item")[:numberOfItemsToFetch]

        for index, item in enumerate(items):
            enclosure = item.find(".//enclosure")
            episodeLink = enclosure.get("url") if enclosure is not None else "No Episode Link Found"

            itemGuid = find_element(item, ["guid"])
            itemGuid = itemGuid.text if itemGuid is not None else f"no-guid-{index}"

            pubDateElement = find_element(item, ["pubDate"])
            pubDateString = pubDateElement.text if pubDateElement is not None else datetime.now().strftime("%a, %d %b %Y %H:%M:%S %z")
            pubDate = BaseDataSourcePlugin.parseDate(pubDateString).replace(tzinfo=pytz.UTC)

            episodeTitle = find_element(item, ["title"])
            episodeTitle = episodeTitle.text if episodeTitle is not None else f"Untitled Episode {index + 1}"

            if (lastFetched and pubDate > lastFetched) or not lastFetched:
                segments.append(
                    PodcastStory(
                        itemOrder=index + 1,
                        title=episodeTitle,
                        link=episodeLink,
                        source=(podcastTitle.text if hasattr(podcastTitle, "text") else str(podcastTitle)),
                        podcastEpisodeLink=episodeLink,
                        uniqueId=BaseDataSourcePlugin.url_to_filename(itemGuid),
                        rootLink=cleanLink,
                        pubDate=pubDate.isoformat(),
                    ).to_dict()
                )

        return segments

    def writePodcastDetails(self, podcastName, segments):
        copiedTopStories = copy.deepcopy(segments)
        for item in copiedTopStories:
            if "podcastEpisodeLink" in item:
                item["link"] = item["podcastEpisodeLink"]
            elif "link" in item:
                item["podcastEpisodeLink"] = item["link"]
        os.makedirs(podcastName, exist_ok=True)
        with open(podcastName + "/podcastDetails.json", "w", encoding="utf-8") as file:
            json.dump(copiedTopStories, file)


plugin = PodcastFeedDataSourcePlugin()
