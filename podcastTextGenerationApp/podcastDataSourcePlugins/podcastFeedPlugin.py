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
            response = requests.get(feedUrl, timeout=10)
            root = ET.fromstring(response.content)
            namespace = {
                "podcast": "https://github.com/Podcastindex-org/podcast-namespace/blob/main/docs/1.0.md"
            }
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
                namespace,
                podcastTitle,
                cleanLink,
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
        self,
        lastFetched,
        numberOfItemsToFetch,
        stories: list,
        root,
        namespace,
        podcastTitle,
        cleanLink,
    ):
        for index, item in enumerate(root.findall(".//item")[:numberOfItemsToFetch]):
            altItem = root.find(".//item")
            episodeLinkObj = item.find("link")
            episodeLink = "No Episode Link Found"
            if episodeLinkObj is None:
                episodeLinkObj = altItem.find("link")
                if hasattr(episodeLinkObj, "text"):
                    episodeLink = episodeLinkObj.text
            transcript = item.find("podcast:transcript", namespace)
            if transcript is None:
                transcript = altItem.find(
                    ".//{https://podcastindex.org/namespace/1.0}transcript"
                )
            itemGuid = item.find("guid").text
            pubDateString = item.find("pubDate").text
            pubDate = self.parseDate(pubDateString)
            pubDate = pubDate.replace(tzinfo=pytz.UTC)
            podcastOrder = index + 1
            episodeTitle = item.find("title")
            if episodeTitle is None:
                episodeTitle = altItem.find("title")
            if transcript is not None:
                if (lastFetched and pubDate > lastFetched) or not lastFetched:
                    stories.append(
                        PodcastStory(
                            podcastOrder=podcastOrder,
                            title=episodeTitle.text,
                            link=transcript.get("url"),
                            storyType="Podcast",
                            source=podcastTitle.text,
                            podcastEpisodeLink=episodeLink,
                            uniqueId=self.url_to_filename(itemGuid),
                            rootLink=cleanLink,
                            pubDate=pubDate.isoformat(),
                        ).to_dict()
                    )

    def writePodcastDetails(self, podcastName, stories):
        copiedTopStories = copy.deepcopy(stories)
        for item in copiedTopStories:
            item["link"] = item["podcastEpisodeLink"]
        os.makedirs(podcastName, exist_ok=True)
        with open(podcastName + "/podcastDetails.json", "w", encoding="utf-8") as file:
            json.dump(copiedTopStories, file)


plugin = PodcastTranscriptAPIPlugin()
