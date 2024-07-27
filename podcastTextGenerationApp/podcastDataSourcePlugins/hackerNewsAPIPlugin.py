import json
import os

import requests
from podcastDataSourcePlugins.baseDataSourcePlugin import BaseDataSourcePlugin
from podcastDataSourcePlugins.models.hackerNewsStory import HackerNewsStory


class HackerNewsAPIPlugin(BaseDataSourcePlugin):
    def __init__(self):
        super().__init__()
        self.baseUrl = "https://hacker-news.firebaseio.com/v0/"

    def identify(self) -> str:
        return "🧑‍💻 Hacker News API Plugin"

    def fetchStories(self):
        topStoriesUrl = f"{self.baseUrl}topstories.json"
        response = requests.get(topStoriesUrl, timeout=10)
        topStoriesIds = response.json()

        stories = []

        for rank, storyId in enumerate(topStoriesIds[:5]):
            storyUrl = f"{self.baseUrl}item/{storyId}.json"
            response = requests.get(storyUrl, timeout=10)
            storyData = response.json()

            story = HackerNewsStory(
                newsRank=rank,
                title=storyData.get("title"),
                link=storyData.get("url"),
                storyType="Hacker News",
                uniqueId=self.makeUniqueStoryIdentifier(),
            )
            stories.append(story.to_dict())

        return stories

    def writePodcastDetails(self, podcastName, stories):
        os.makedirs(podcastName, exist_ok=True)
        with open(podcastName + "/podcastDetails.json", "w", encoding="utf-8") as file:
            json.dump(stories, file)


plugin = HackerNewsAPIPlugin()
