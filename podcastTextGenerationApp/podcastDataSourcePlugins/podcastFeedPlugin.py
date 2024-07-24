import copy
import json
import os
import re
from datetime import datetime
from urllib.parse import urlparse
from xml.etree import ElementTree as ET
import pytz
import requests
from dateutil.parser import parse
from firebase_admin import db
from podcastDataSourcePlugins.baseDataSourcePlugin import BaseDataSourcePlugin
from podcastDataSourcePlugins.models.podcastStory import PodcastStory


class PodcastTranscriptAPIPlugin(BaseDataSourcePlugin):
    def __init__(self):
        super().__init__()
        self.feeds = []

    def identify(self) -> str:
        return "🎙️ Podcast Transcript API Plugin"

    def fetchStories(self):
        lastFetched = None
        ref = None
        podcastFeeds = os.getenv("PODCAST_FEEDS")
        if not podcastFeeds:
            raise ValueError("PODCAST_FEEDS environment variable is not set")

        self.feeds = podcastFeeds.split(",")

        if not self.feeds:
            raise ValueError(
                "No podcast feeds in .env file, please add one and try again."
            )

        numberOfItemsToFetch = int(os.getenv("NUMBER_OF_ITEMS_TO_FETCH"))
        if not numberOfItemsToFetch:
            raise ValueError(
                "NUMBER_OF_ITEMS_TO_FETCH environment variable is not set, please set it and try again."
            )
        stories = []
        # Iterate through each Podcast Feed
        for feedUrl in self.feeds:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
            }
            response = requests.get(feedUrl, headers=headers, timeout=10)
            root = ET.fromstring(response.content)
            rootLink = root.find(".//channel/link").text
            parsedUrl = urlparse(rootLink)
            cleanLink = parsedUrl.netloc + parsedUrl.path
            cleanLink = re.sub(r"\W+", "", cleanLink)

            if self.firebaseServiceAccountKeyPath:
                ref = db.reference(f"podcast/{cleanLink}/")
                lastFetched = ref.get()
                if lastFetched:
                    lastFetched = parse(lastFetched["lastFetched"])

            podcastTitle = root.find(".//channel/title")
            # Iterate through each podcast episode
            self.getStoriesFromFeed(
                lastFetched,
                numberOfItemsToFetch,
                stories,
                root,
                podcastTitle,
                cleanLink,
            )
        if len(stories) > 0:
            # Sort the stories by publication date in descending order
            stories.sort(key=lambda x: x["pubDate"], reverse=True)
            mostRecentStory = stories[0]
            mostRecentTimestamp = mostRecentStory["pubDate"]
            if ref:
                ref.set({"lastFetched": mostRecentTimestamp})
            return stories
        return []

    def getStoriesFromFeed(
        self,
        lastFetched,
        numberOfItemsToFetch,
        stories: list,
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
            episodeLink = (
                enclosure.get("url")
                if enclosure is not None
                else "No Episode Link Found"
            )

            itemGuid = find_element(item, ["guid"])
            itemGuid = itemGuid.text if itemGuid is not None else f"no-guid-{index}"

            pubDateElement = find_element(item, ["pubDate"])
            pubDateString = (
                pubDateElement.text
                if pubDateElement is not None
                else datetime.now().strftime("%a, %d %b %Y %H:%M:%S %z")
            )
            pubDate = self.parseDate(pubDateString).replace(tzinfo=pytz.UTC)

            episodeTitle = find_element(item, ["title"])
            episodeTitle = (
                episodeTitle.text
                if episodeTitle is not None
                else f"Untitled Episode {index + 1}"
            )

            if (lastFetched and pubDate > lastFetched) or not lastFetched:
                stories.append(
                    PodcastStory(
                        itemOrder=index + 1,
                        title=episodeTitle,
                        link=episodeLink,
                        source=(
                            podcastTitle.text
                            if hasattr(podcastTitle, "text")
                            else str(podcastTitle)
                        ),
                        podcastEpisodeLink=episodeLink,
                        uniqueId=self.url_to_filename(itemGuid),
                        rootLink=cleanLink,
                        pubDate=pubDate.isoformat(),
                    ).to_dict()
                )

        return stories

    def writePodcastDetails(self, podcastName, stories):
        copiedTopStories = copy.deepcopy(stories)
        for item in copiedTopStories:
            if "podcastEpisodeLink" in item:
                item["link"] = item["podcastEpisodeLink"]
            elif "link" in item:
                item["podcastEpisodeLink"] = item["link"]
        os.makedirs(podcastName, exist_ok=True)
        with open(podcastName + "/podcastDetails.json", "w", encoding="utf-8") as file:
            json.dump(copiedTopStories, file)


plugin = PodcastTranscriptAPIPlugin()
