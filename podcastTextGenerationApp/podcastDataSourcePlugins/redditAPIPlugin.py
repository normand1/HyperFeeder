from podcastDataSourcePlugins.abstractPluginDefinitions.abstractDataSourcePlugin import (
    AbstractDataSourcePlugin,
)
import requests
import os
import json

from podcastDataSourcePlugins.models.redditStory import RedditStory


class RedditAPIPlugin(AbstractDataSourcePlugin):
    def __init__(self):
        super().__init__()
        subreddit = os.getenv("SUBREDDIT")
        if not subreddit:
            raise ValueError(
                "SUBREDDIT environment variable is not set, please set it and try again."
            )
        self.base_url = f"https://www.reddit.com/r/{subreddit}.json"

    def identify(self) -> str:
        return "🗞️ Reddit API Plugin"

    def fetchStories(self):
        response = requests.get(self.base_url, headers={"User-agent": "Mozilla/5.0"})
        data = response.json()

        stories = []

        for rank, post in enumerate(data["data"]["children"][:5]):
            story = RedditStory(
                newsRank=rank,
                title=post["data"].get("title"),
                link=post["data"].get("url"),
                storyType=post["data"].get(
                    "post_hint", "text"
                ),  # Default to 'text' if no post_hint.
                uniqueId=self.makeUniqueStoryIdentifier(),
            )
            stories.append(story.to_dict())

        return stories

    def writePodcastDetails(self, podcastName, stories):
        os.makedirs(podcastName, exist_ok=True)
        with open(podcastName + "/podcastDetails.json", "w") as file:
            json.dump(stories, file)


plugin = RedditAPIPlugin()
