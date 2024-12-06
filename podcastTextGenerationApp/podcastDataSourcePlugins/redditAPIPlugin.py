import json
import os

import requests
from podcastDataSourcePlugins.baseDataSourcePlugin import BaseDataSourcePlugin
from podcastDataSourcePlugins.models.redditStory import RedditStory


class RedditAPIPlugin(BaseDataSourcePlugin):
    def __init__(self):
        super().__init__()
        subreddits = os.getenv("SUBREDDIT")
        if not subreddits:
            raise ValueError("SUBREDDIT environment variable is not set, please set it and try again.")
        self.subreddits = [s.strip() for s in subreddits.split(",")]
        self.baseUrl = "https://www.reddit.com/r/{}.json"

    def identify(self) -> str:
        return "👽 Reddit API Plugin"

    def fetchStories(self):
        stories = []
        numberOfPostsToFetch = int(os.getenv("NUMBER_OF_POSTS_TO_FETCH"))

        for subreddit in self.subreddits:
            response = requests.get(
                self.baseUrl.format(subreddit),
                headers={"User-agent": "Mozilla/5.0"},
                timeout=10,
            )
            data = response.json()

            rank = 0
            for post in data["data"]["children"]:
                if (
                    post["data"].get("author") != "AutoModerator"
                    and post["data"].get("link_flair_text") != "Subreddit Stats"
                    and "reddit.com" not in post["data"].get("url")
                    and not post["data"].get("is_video")
                ):
                    if rank >= numberOfPostsToFetch:
                        break
                    story = RedditStory(
                        newsRank=rank,
                        title=post["data"].get("title"),
                        link=post["data"].get("url"),
                        storyType="Reddit",
                        uniqueId=self.makeUniqueStoryIdentifier(),
                    )
                    stories.append(story.to_dict())
                    rank += 1

        return stories

    def writePodcastDetails(self, podcastName, stories):
        os.makedirs(podcastName, exist_ok=True)
        with open(podcastName + "/podcastDetails.json", "w", encoding="utf-8") as file:
            json.dump(stories, file)


plugin = RedditAPIPlugin()
