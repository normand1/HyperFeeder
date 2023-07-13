import json
import os

import requests
from podcastDataSourcePlugins.baseDataSourcePlugin import BaseDataSourcePlugin
from podcastDataSourcePlugins.models.redditStory import RedditStory


class RedditAPIPlugin(BaseDataSourcePlugin):
    def __init__(self):
        super().__init__()
        subreddit = os.getenv("SUBREDDIT")
        if not subreddit:
            raise ValueError(
                "SUBREDDIT environment variable is not set, please set it and try again."
            )
        self.baseUrl = f"https://www.reddit.com/r/{subreddit}.json"

    def identify(self) -> str:
        return "👽 Reddit API Plugin"

    def fetchStories(self):
        response = requests.get(
            self.baseUrl, headers={"User-agent": "Mozilla/5.0"}, timeout=10
        )
        data = response.json()

        stories = []
        numberOfPostsToFetch = int(os.getenv("NUMBER_OF_POSTS_TO_FETCH"))
        for rank, post in enumerate(data["data"]["children"][:numberOfPostsToFetch]):
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
        with open(podcastName + "/podcastDetails.json", "w", encoding="utf-8") as file:
            json.dump(stories, file)


plugin = RedditAPIPlugin()
