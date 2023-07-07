from podcastDataSourcePlugins.baseDataSourcePlugin import BaseDataSourcePlugin
import requests
from xml.etree import ElementTree as ET
from podcastDataSourcePlugins.models.podcastStory import PodcastStory
import os
import json
import copy


class PodcastTranscriptAPIPlugin(BaseDataSourcePlugin):
    def __init__(self):
        super().__init__()
        self.feeds = []

    def identify(self) -> str:
        return "🎙️ Podcast Transcript API Plugin"

    def fetchStories(self):
        podcast_feeds = os.getenv("PODCAST_FEEDS")
        if not podcast_feeds:
            raise ValueError("PODCAST_FEEDS environment variable is not set")

        self.feeds = podcast_feeds.split(",")

        if not self.feeds:
            raise ValueError(
                "No podcast feeds in .env file, please add one and try again."
            )
        stories = []
        for index, feed_url in enumerate(self.feeds):
            response = requests.get(feed_url)
            root = ET.fromstring(response.content)
            namespace = {
                "podcast": "https://github.com/Podcastindex-org/podcast-namespace/blob/main/docs/1.0.md"
            }

            podcast_title = root.find(".//channel/title")
            firstItem = list(root.iterfind(".//channel/item", namespace))[0]
            altItem = root.find(".//item")
            episodeLinkObj = firstItem.find("link")
            episodeLink = "No Episode Link Found"
            if episodeLinkObj is None:
                episodeLinkObj = altItem.find("link")
                if hasattr(episodeLinkObj, "text"):
                    episodeLink = episodeLinkObj.text
            transcript = firstItem.find("podcast:transcript", namespace)
            if transcript is None:
                transcript = altItem.find(
                    ".//{https://podcastindex.org/namespace/1.0}transcript"
                )
            podcastOrder = index + 1
            episodeTitle = firstItem.find("title")
            if episodeTitle is None:
                episodeTitle = altItem.find("title")
            if transcript is not None:
                stories.append(
                    PodcastStory(
                        podcastOrder=podcastOrder,
                        title=episodeTitle.text,
                        link=transcript.get("url"),
                        storyType="Podcast",
                        source=podcast_title.text,
                        podcastEpisodeLink=episodeLink,
                        uniqueId=self.makeUniqueStoryIdentifier(),
                    ).to_dict()
                )
        return stories

    def writePodcastDetails(self, podcastName, stories):
        copiedTopStories = copy.deepcopy(stories)
        for item in copiedTopStories:
            item["link"] = item["podcastEpisodeLink"]
        os.makedirs(podcastName, exist_ok=True)
        with open(podcastName + "/podcastDetails.json", "w") as file:
            json.dump(copiedTopStories, file)


plugin = PodcastTranscriptAPIPlugin()
