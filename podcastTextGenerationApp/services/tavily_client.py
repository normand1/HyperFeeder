import os

from tavily import TavilyClient
from utilities.cache_manager import SimpleCacheManager


class CachedTavilyClient:
    def __init__(self):
        self._client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        self._cache = SimpleCacheManager("cache/tavily", "search_cache.json")

    def search(self, query: str) -> list:
        """
        Performs a cached search using the Tavily API
        """
        if cached_results := self._cache.get(query):
            return cached_results

        results = self._client.search(query)["results"]
        self._cache.set(query, results)
        return results
