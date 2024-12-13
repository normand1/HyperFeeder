import requests
from typing import Optional, Dict, Any, Union, List
import os
from dotenv import load_dotenv
import click
import requests_cache


class NeynarAPIManager:
    """Manages interactions with the Neynar API for Farcaster data."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Neynar API manager.

        Args:
            api_key: Optional API key. If not provided, will try to load from environment variables.
        """
        load_dotenv()
        self.api_key = api_key or os.getenv("NEYNAR_API_KEY")
        if not self.api_key:
            raise ValueError("Neynar API key is required. Provide it directly or set NEYNAR_API_KEY environment variable.")

        self.base_url = "https://api.neynar.com/v2/farcaster"
        self.headers = {"accept": "application/json", "x-neynar-experimental": "true", "x-api-key": self.api_key}

        # Initialize requests-cache with a 24-hour expiration
        requests_cache.install_cache("neynar_cache", expire_after=86400)

    def get_user_by_username(self, username: str) -> Dict[str, Any]:
        """
        Fetch user information from Neynar API by username.

        Args:
            username: The Farcaster username to look up

        Returns:
            Dict containing the user information

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        url = f"{self.base_url}/user/by_username"
        params = {"username": username}

        response = requests.get(url, headers=self.headers, params=params, timeout=10)
        response.raise_for_status()

        # Log whether the response was from cache or not
        if response.from_cache:
            print(f"Cache used for username: {username}")
        else:
            print(f"Data refetched for username: {username}")

        return response.json()

    def search_casts(self, query: str, priority_mode: bool = False, limit: int = 5, author_fid: Optional[str] = None) -> Dict[str, Any]:
        """
        Search for casts using a query string.

        Args:
            query: The search query string
            priority_mode: Whether to use priority mode for search results (default: False)
            limit: Maximum number of results to return (default: 25)
            author_fid: Optional UUID of the author to filter results

        Returns:
            Dict containing the search results

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        url = f"{self.base_url}/cast/search"
        params = {"q": query, "priority_mode": str(priority_mode).lower(), "limit": limit}
        if author_fid:
            params["author_fid"] = author_fid

        response = requests.get(url, headers=self.headers, params=params, timeout=10)
        response.raise_for_status()
        print(response.json())

        # Log whether the response was from cache or not
        if response.from_cache:
            print(f"Cache used for search query: {query}")
        else:
            print(f"Data refetched for search query: {query}")

        return response.json()["result"]

    def post_cast(self, text: str, signer_uuid: Optional[str] = None, frame_url: Optional[str] = None, reply_to: Optional[str] = None) -> Dict[str, Any]:
        """
        Post a new cast to Farcaster.

        Args:
            text: The text content of the cast
            signer_uuid: The UUID of the signer. If not provided, will try to load from environment variables.
            frame_url: The URL of the frame to embed in the cast.
            reply_to: The hash of the cast to reply to.

        Returns:
            Dict containing the API response

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If signer_uuid is not provided or found in environment
        """
        url = f"{self.base_url}/cast"

        # Get signer_uuid from params or environment
        signer_uuid = signer_uuid or os.getenv("NEYNAR_SIGNER_UUID")
        if not signer_uuid:
            raise ValueError("Signer UUID is required. Provide it directly or set NEYNAR_SIGNER_UUID environment variable.")

        click.echo(f"Posting cast with frameurl: {frame_url}")
        # Prepare the payload with optional frame_url and reply_to
        payload = {
            "signer_uuid": signer_uuid,
            "text": text,
            "embeds": [{"url": frame_url}] if frame_url else [],
        }
        if reply_to:
            payload["reply_to"] = reply_to

        headers = {**self.headers, "content-type": "application/json"}

        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()

        return response.json()

    def get_trending_feed(self, limit: int = 10, time_window: str = "24h", channel_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Fetch trending casts from Farcaster.

        Args:
            limit: Maximum number of results to return (default: 10)
            time_window: Time window for trending casts (default: "24h")
            channel_id: Optional channel ID to filter results (e.g. "founders")

        Returns:
            Dict containing the trending feed results

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        url = f"{self.base_url}/feed/trending"
        params = {"limit": limit, "time_window": time_window, "provider": "neynar"}
        if channel_id:
            params["channel_id"] = channel_id

        response = requests.get(url, headers=self.headers, params=params, timeout=10)
        response.raise_for_status()

        # Log whether the response was from cache or not
        if response.from_cache:
            print(f"Cache used for trending feed")
        else:
            print(f"Data refetched for trending feed")

        return response.json()["casts"]

    def get_channel_feed(self, channel_ids: Union[str, List[str]], limit: int = 5, with_recasts: bool = True, with_replies: bool = True, members_only: bool = True) -> Dict[str, Any]:
        """
        Fetch feed based on channel IDs from Farcaster.

        Args:
            channel_ids: Single channel ID or list of channel IDs (e.g. "orange-dao")
            limit: Maximum number of results to return (default: 5)
            with_recasts: Include recasts in results (default: True)
            with_replies: Include replies in results (default: True)
            members_only: Only show casts from channel members (default: True)

        Returns:
            Dict containing the channel feed results

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        url = f"{self.base_url}/feed/channels"

        # Convert list of channel IDs to comma-separated string if needed
        if isinstance(channel_ids, list):
            channel_ids = ",".join(channel_ids)

        params = {"channel_ids": channel_ids, "with_recasts": str(with_recasts).lower(), "with_replies": str(with_replies).lower(), "members_only": str(members_only).lower(), "limit": limit}

        response = requests.get(url, headers=self.headers, params=params, timeout=10)
        response.raise_for_status()

        # Log whether the response was from cache or not
        if response.from_cache:
            print(f"Cache used for channel feed: {channel_ids}")
        else:
            print(f"Data refetched for channel feed: {channel_ids}")

        return response.json()
