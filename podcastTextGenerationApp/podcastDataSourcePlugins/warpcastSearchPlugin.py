import json
import os

from podcastDataSourcePlugins.baseDataSourcePlugin import BaseDataSourcePlugin
from sharedPluginServices.neynarAPIManager import NeynarAPIManager
from langchain_core.tools import tool
from colorama import Fore, Style
from podcastDataSourcePlugins.models.warpcastStory import WarpcastStory


class WarpcastSearchPlugin(BaseDataSourcePlugin):
    def __init__(self):
        super().__init__()
        self._neynar_api_manager = NeynarAPIManager()

    @classmethod
    def identify(cls, simpleName=False) -> str:
        if simpleName:
            return "warpcastSearch"
        else:
            return "🔍 Warpcast Search Plugin"

    @staticmethod
    @tool(name_or_callable="WarpcastSearchPlugin-_-searchCasts")
    def searchCasts(searchQuery: str = None) -> list[WarpcastStory]:
        """
        Search for casts (tweets) on the crypto social media platform Warpcast
        """
        # Get the number of posts to fetch from config
        number_of_posts = 2  # TODO: Default value, should be configured in values yaml

        # Use the Neynar API to search for casts
        neynar_api_manager = NeynarAPIManager()
        search_results = neynar_api_manager.search_casts(searchQuery, limit=number_of_posts)

        segments = []
        for cast in search_results["casts"]:
            # Convert the cast dict to a WarpcastStory object
            story_dict = {
                "content": json.dumps(cast),
                "url": f"https://warpcast.com/{cast.get('author', {}).get('username')}/{cast.get('hash')}",
                "timestamp": cast.get("timestamp"),
                "hash": cast.get("hash"),
            }
            segments.append(WarpcastStory.from_dict(story_dict))

        print(f"{Fore.GREEN}{Style.BRIGHT}Fetched {len(segments)} segments from Warpcast{Style.RESET_ALL}")
        return segments

    def writePodcastDetails(self, podcastName, segments):
        os.makedirs(podcastName, exist_ok=True)
        with open(podcastName + "/podcastDetails.json", "w", encoding="utf-8") as file:
            json.dump(segments, file)

    def filterForImportantContextOnly(self, subStoryContent: dict):
        keysToKeep = ["author", "content", "timestamp", "reactions", "replies", "mentioned_profiles"]
        return {key: subStoryContent[key] for key in keysToKeep if key in subStoryContent}

    @staticmethod
    @tool(name_or_callable="WarpcastSearchPlugin-_-getUserByUsername")
    def getUserByUsername(username: str):
        """
        Get user information from Warpcast by their username
        """
        neynar_api_manager = NeynarAPIManager()
        user_info = neynar_api_manager.get_user_by_username(username)

        print(f"{Fore.GREEN}{Style.BRIGHT}Fetched user info for {username} from Warpcast{Style.RESET_ALL}")
        return user_info

    @staticmethod
    @tool(name_or_callable="WarpcastSearchPlugin-_-getTrendingFeed")
    def getTrendingFeed(limit: int = 10, time_window: str = "24h", channel_id: str = None):
        """
        Get trending casts from Warpcast within a specified time window
        Args:
            limit: Maximum number of results to return (default: 10)
            time_window: Time window for trending casts (default: "24h")
            channel_id: Optional channel to filter results (e.g. "founders")
        """
        neynar_api_manager = NeynarAPIManager()
        trending_feed = neynar_api_manager.get_trending_feed(limit=limit, time_window=time_window, channel_id=channel_id)

        segments = []
        for cast in trending_feed:
            # Convert the cast dict to a WarpcastStory object
            story_dict = {
                "content": json.dumps(cast),
                "url": f"https://warpcast.com/{cast.get('author', {}).get('username')}/{cast.get('hash')}",
                "timestamp": cast.get("timestamp"),
                "hash": cast.get("hash"),
            }
            segments.append(WarpcastStory.from_dict(story_dict))

        print(f"{Fore.GREEN}{Style.BRIGHT}Fetched {len(segments)} trending casts from Warpcast{Style.RESET_ALL}")
        return segments

    def fetchContentForStory(self, story: WarpcastStory):
        return story.content


plugin = WarpcastSearchPlugin()
