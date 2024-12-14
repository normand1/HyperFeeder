import os
import json
from typing import Dict, Any, Optional


class SimpleCacheManager:
    """A generic cache manager for storing and retrieving JSON-serializable data."""

    def __init__(self, cache_dir: str, cache_filename: str):
        """
        Initialize the cache manager.

        Args:
            cache_dir: Directory to store the cache file
            cache_filename: Name of the cache file
        """
        self._cache_dir = cache_dir
        self._cache_file = os.path.join(cache_dir, cache_filename)
        os.makedirs(cache_dir, exist_ok=True)
        self._cache = self._load_cache()

    def _load_cache(self) -> Dict[str, Any]:
        """Load the cache from disk."""
        try:
            with open(self._cache_file, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _save_cache(self) -> None:
        """Save the cache to disk."""
        with open(self._cache_file, "w") as f:
            json.dump(self._cache, f)

    def get(self, key: str) -> Optional[Any]:
        """
        Retrieve a value from the cache.

        Args:
            key: Cache key to lookup

        Returns:
            The cached value if found, None otherwise
        """
        return self._cache.get(key)

    def set(self, key: str, value: Any) -> None:
        """
        Store a value in the cache.

        Args:
            key: Cache key
            value: Value to store (must be JSON-serializable)
        """
        self._cache[key] = value
        self._save_cache()

    def has(self, key: str) -> bool:
        """
        Check if a key exists in the cache.

        Args:
            key: Cache key to check

        Returns:
            True if the key exists, False otherwise
        """
        return key in self._cache
