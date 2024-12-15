import json
import os

from podcastDataSourcePlugins.baseDataSourcePlugin import BaseDataSourcePlugin
from sharedPluginServices.neynarAPIManager import NeynarAPIManager
from langchain_core.tools import tool
from colorama import Fore, Style
from podcastDataSourcePlugins.models.warpcastStory import WarpcastStory


class WarpcastDataSourcePlugin(BaseDataSourcePlugin):
    def __init__(self):
        super().__init__()
        self._neynarApiManager = NeynarAPIManager()

    @classmethod
    def identify(cls, simpleName=False) -> str:
        if simpleName:
            return "warpcastSearch"
        else:
            return "🔍 Warpcast Search Plugin"

    @staticmethod
    @tool(name_or_callable="WarpcastDataSourcePlugin-_-searchCasts")
    def searchCasts(searchQuery: str = None) -> list[WarpcastStory]:
        """
        Search for casts (tweets) on the crypto social media platform Warpcast
        """
        # Get the number of posts to fetch from config
        numberOfPosts = os.getenv("WARPCAST_SEARCH_NUMBER_OF_POSTS_TO_FETCH")

        # Use the Neynar API to search for casts
        neynarApiManager = NeynarAPIManager()
        search_results = neynarApiManager.search_casts(searchQuery, limit=numberOfPosts)

        segments = []
        for cast in search_results["casts"]:
            cast = WarpcastDataSourcePlugin.filterCast(cast)
            # Convert the cast dict to a WarpcastStory object
            storyDict = {
                "content": json.dumps(cast),
                "url": f"https://warpcast.com/{cast.get('author', {}).get('username')}/{cast.get('hash')}",
                "timestamp": cast.get("timestamp"),
                "hash": cast.get("hash"),
            }
            segments.append(WarpcastStory.from_dict(storyDict))

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
    @tool(name_or_callable="WarpcastDataSourcePlugin-_-getUserByUsername")
    def getUserByUsername(username: str):
        """
        Get user information from Warpcast by their username
        """
        neynarApiManager = NeynarAPIManager()
        userInfo = neynarApiManager.get_user_by_username(username)

        print(f"{Fore.GREEN}{Style.BRIGHT}Fetched user info for {username} from Warpcast{Style.RESET_ALL}")
        userInfo = WarpcastDataSourcePlugin.filterUserResponse(userInfo)
        storyDict = {
            "content": json.dumps(userInfo),
            "url": f"https://warpcast.com/{userInfo.get('username')}",
            "timestamp": userInfo.get("timestamp"),
            "hash": userInfo.get("hash"),
        }
        return WarpcastStory.from_dict(storyDict)

    @staticmethod
    @tool(name_or_callable="WarpcastDataSourcePlugin-_-getTrendingFeed")
    def getTrendingFeed(limit: int = 10, time_window: str = "24h", channel_id: str = None):
        """
        Get trending casts from Warpcast within a specified time window
        Args:
            limit: Maximum number of results to return (default: 10)
            time_window: Time window for trending casts (default: "24h")
            channel_id: Optional channel to filter results (e.g. "founders")
        """
        neynarApiManager = NeynarAPIManager()
        trending_feed = neynarApiManager.get_trending_feed(limit=limit, time_window=time_window, channel_id=channel_id)
        trending_feed = WarpcastDataSourcePlugin.filterTrendingFeedResponse(trending_feed)
        segments = []
        for cast in trending_feed:
            storyDict = {
                "content": json.dumps(cast),
                "url": f"https://warpcast.com/{cast.get('author', {}).get('username')}/{cast.get('hash')}",
                "timestamp": cast.get("timestamp"),
                "hash": cast.get("hash"),
            }
            segments.append(WarpcastStory.from_dict(storyDict))

        print(f"{Fore.GREEN}{Style.BRIGHT}Fetched {len(segments)} trending casts from Warpcast{Style.RESET_ALL}")
        return segments

    def fetchContentForStory(self, story: WarpcastStory):
        return story.content

    @staticmethod
    @tool(name_or_callable="WarpcastDataSourcePlugin-_-getChannelFeed")
    def getChannelFeed(channel_ids: str, limit: int = 5, with_recasts: bool = True, with_replies: bool = True, members_only: bool = True) -> list[WarpcastStory]:
        """
        Get feed from specific Warpcast channels
        Args:
            channel_ids: Channel ID or comma-separated list of channel IDs (e.g. "orange-dao" or "orange-dao,founders")
            limit: Maximum number of results to return (default: 5)
            with_recasts: Include recasts in results (default: True)
            with_replies: Include replies in results (default: True)
            members_only: Only show casts from channel members (default: True)
        """
        neynarApiManager = NeynarAPIManager()
        channel_feed = neynarApiManager.get_channel_feed(channel_ids=channel_ids, limit=limit, with_recasts=with_recasts, with_replies=with_replies, members_only=members_only)
        channel_feed = WarpcastDataSourcePlugin.filterChannelFeedResponse(channel_feed)
        segments = []
        for cast in channel_feed:
            # Convert the cast dict to a WarpcastStory object
            storyDict = {
                "content": json.dumps(cast),
                "url": f"https://warpcast.com/{cast.get('author', {}).get('username')}/{cast.get('hash')}",
                "timestamp": cast.get("timestamp"),
                "hash": cast.get("hash"),
            }
            segments.append(WarpcastStory.from_dict(storyDict))

        print(f"{Fore.GREEN}{Style.BRIGHT}Fetched {len(segments)} casts from Warpcast channels: {channel_ids}{Style.RESET_ALL}")
        return segments

    @staticmethod
    def filterCast(cast):
        # Extract fields that matter to telling the story
        # Avoid hash, parent_hash, urls, fids, etc.
        filtered = {}
        filtered["text"] = cast.get("text")
        filtered["timestamp"] = cast.get("timestamp")

        author = cast.get("author", {})
        filtered["author"] = {"username": author.get("username"), "display_name": author.get("display_name"), "bio": author.get("profile", {}).get("bio", {}).get("text")}

        # Keep mentions only as basic references
        filtered["mentioned_profiles"] = []
        for m in cast.get("mentioned_profiles", []):
            filtered["mentioned_profiles"].append({"username": m.get("username"), "display_name": m.get("display_name")})

        # Keep simple counts of reactions and replies for story context
        reactions = cast.get("reactions", {})
        filtered["likes_count"] = reactions.get("likes_count")
        filtered["recasts_count"] = reactions.get("recasts_count")

        replies = cast.get("replies", {})
        filtered["replies_count"] = replies.get("count")

        return filtered

    @staticmethod
    def filterUserResponse(user_data):
        user = user_data.get("user", {})
        filtered = {}
        filtered["username"] = user.get("username")
        filtered["display_name"] = user.get("display_name")
        filtered["bio"] = user.get("profile", {}).get("bio", {}).get("text")
        filtered["follower_count"] = user.get("follower_count")
        filtered["following_count"] = user.get("following_count")
        return filtered

    @staticmethod
    def filterTrendingFeedResponse(trending_feed_data):
        filtered_casts = []
        for cast in trending_feed_data.get("casts", []):
            filtered = {}
            filtered["text"] = cast.get("text")
            filtered["timestamp"] = cast.get("timestamp")
            author = cast.get("author", {})
            filtered["author"] = {"username": author.get("username"), "display_name": author.get("display_name"), "bio": author.get("profile", {}).get("bio", {}).get("text")}

            filtered["mentioned_profiles"] = []
            for m in cast.get("mentioned_profiles", []):
                filtered["mentioned_profiles"].append({"username": m.get("username"), "display_name": m.get("display_name")})

            reactions = cast.get("reactions", {})
            filtered["likes_count"] = reactions.get("likes_count")
            filtered["recasts_count"] = reactions.get("recasts_count")

            replies = cast.get("replies", {})
            filtered["replies_count"] = replies.get("count")

            filtered_casts.append(filtered)

        return {"casts": filtered_casts, "next": trending_feed_data.get("next")}

    @staticmethod
    def filterChannelFeedResponse(channel_feed_data):
        # If channel_feed_data is a list of casts rather than a dict with a "casts" key,
        # adjust accordingly. If it's a dict, use channel_feed_data.get("casts", []).
        if isinstance(channel_feed_data, dict):
            casts = channel_feed_data.get("casts", [])
            next_val = channel_feed_data.get("next")
        else:
            # If channel_feed_data is a list, assume it's directly a list of casts
            casts = channel_feed_data
            next_val = None

        filtered_casts = []
        for cast in casts:
            filtered = {}
            filtered["text"] = cast.get("text")
            filtered["timestamp"] = cast.get("timestamp")
            author = cast.get("author", {})
            filtered["author"] = {"username": author.get("username"), "display_name": author.get("display_name"), "bio": author.get("profile", {}).get("bio", {}).get("text")}

            filtered["mentioned_profiles"] = []
            for m in cast.get("mentioned_profiles", []):
                filtered["mentioned_profiles"].append({"username": m.get("username"), "display_name": m.get("display_name")})

            reactions = cast.get("reactions", {})
            filtered["likes_count"] = reactions.get("likes_count")
            filtered["recasts_count"] = reactions.get("recasts_count")

            replies = cast.get("replies", {})
            filtered["replies_count"] = replies.get("count")

            filtered_casts.append(filtered)

        return filtered_casts


plugin = WarpcastDataSourcePlugin()
