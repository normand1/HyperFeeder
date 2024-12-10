import json
import os

import requests
from podcastDataSourcePlugins.baseDataSourcePlugin import BaseDataSourcePlugin
from podcastDataSourcePlugins.models.redditStory import RedditStory
from langchain_core.tools import tool
from podcastScraperPlugins.newsStoryScraperPlugin import NewsStoryScraperPlugin
from colorama import Fore, Style


class RedditDataSourcePlugin(BaseDataSourcePlugin):

    def __init__(self):
        super().__init__()
        self.scraperPlugin = NewsStoryScraperPlugin()

    @classmethod
    def identify(cls, simpleName=False) -> str:
        if simpleName:
            return "reddit"
        else:
            return "👽 Reddit API Plugin"

    @staticmethod
    @tool(name_or_callable="RedditDataSourcePlugin-_-getTopPosts")
    def getTopPosts(subreddits: list[str] = None) -> list[RedditStory]:
        """Get the top posts from a list of subreddits"""
        stories = []
        baseUrl = "https://www.reddit.com/r/{}.json"
        numberOfPostsToFetch = int(os.getenv("NUMBER_OF_SUBREDDIT_POSTS_TO_FETCH"))

        for subreddit in subreddits:
            response = requests.get(
                baseUrl.format(subreddit),
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
                        content="",
                        raw_content="",
                        uniqueId=RedditDataSourcePlugin.makeUniqueStoryIdentifier(),
                    )
                    stories.append(story)
                    rank += 1
        print(f"{Fore.GREEN}{Style.BRIGHT}Fetched {len(stories)} stories from Reddit{Style.RESET_ALL}")
        return stories

    def fetchContentForStory(self, story: RedditStory):
        return self.scraperPlugin.scrapeStoryText(story.link)

    def writePodcastDetails(self, podcastName, stories):
        os.makedirs(podcastName, exist_ok=True)
        with open(podcastName + "/podcastDetails.json", "w", encoding="utf-8") as file:
            json.dump(stories, file)

    def filterForImportantContextOnly(self, subStoryContent: dict):
        keysToKeep = ["title", "content"]
        return {key: subStoryContent[key] for key in keysToKeep if key in subStoryContent}


plugin = RedditDataSourcePlugin()
