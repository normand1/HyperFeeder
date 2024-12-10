class Story:
    def __init__(self, newsRank, title, link, storyType, uniqueId, source):
        self.newsRank = newsRank
        self.title = title
        self.link = link
        self.storyType = storyType
        self.source = source
        self.uniqueId = uniqueId
        self.subStories = {}
        self.keysToIgnoreForWritingSegment = [
            "link",
        ]

    def _serialize_sub_stories(self, depth):
        """Helper function to serialize sub-stories with depth control.

        Args:
            depth (int): Maximum depth for serializing nested stories

        Returns:
            dict: Serialized sub-stories dictionary
        """
        serialized = {}
        for key, story_list in self.subStories.items():
            serialized_stories = []
            for story in story_list:
                # Check if story has __json__ method and is not already a dict
                if hasattr(story, "__json__") and not isinstance(story, dict):
                    serialized_stories.append(story.__json__(depth - 1))
                else:
                    # If it's already a dict or doesn't have __json__, use it as-is
                    serialized_stories.append(story)
            serialized[key] = serialized_stories
        return serialized

    def __json__(self, depth=10):
        """Make the class directly JSON serializable

        Args:
            depth (int): Maximum depth for serializing nested stories. Defaults to 10.
        """
        if depth <= 0:  # Base case to prevent infinite recursion
            return {
                "newsRank": self.newsRank,
                "title": self.title,
                "link": self.link,
                "storyType": self.storyType,
                "source": self.source,
                "uniqueId": self.uniqueId,
                "subStories": {},
            }

        return {
            "newsRank": self.newsRank,
            "title": self.title,
            "link": self.link,
            "storyType": self.storyType,
            "source": self.source,
            "uniqueId": self.uniqueId,
            "subStories": self._serialize_sub_stories(depth),
        }

    @classmethod
    def from_dict(cls, story_dict):
        """Factory method to create the appropriate Story subclass based on storyType"""
        story_type = story_dict.get("storyType")

        # Import here to avoid circular imports
        from podcastDataSourcePlugins.models.tokenStory import TokenStory
        from podcastDataSourcePlugins.models.redditStory import RedditStory
        from podcastDataSourcePlugins.models.arxivPaperStory import ArxivPaperStory
        from podcastDataSourcePlugins.models.hackerNewsStory import HackerNewsStory
        from podcastDataSourcePlugins.models.podcastStory import PodcastStory
        from podcastDataSourcePlugins.models.RSSItemStory import RSSItemStory

        # Map story types to their respective classes
        story_classes = {
            "Token": TokenStory,
            "Reddit": RedditStory,
            "ArxivPaper": ArxivPaperStory,
            "HackerNews": HackerNewsStory,
            "Podcast": PodcastStory,
            "RSS": RSSItemStory,
        }

        # Get the appropriate class for the story type
        story_class = story_classes.get(story_type)

        if story_class:
            story = story_class.from_dict(story_dict)
        else:
            # If no specific type or unknown type, create base Story
            story = cls(
                newsRank=story_dict.get("newsRank", 0),
                title=story_dict.get("title", ""),
                link=story_dict.get("link", ""),
                storyType=story_dict.get("storyType", "Unknown"),
                uniqueId=story_dict.get("uniqueId", ""),
                source=story_dict.get("source", "Unknown"),
            )

        # Handle sub-stories if present in the dictionary
        if "subStories" in story_dict:
            story.subStories = {k: [cls.from_dict(sub_story) for sub_story in v] for k, v in story_dict["subStories"].items()}

        # Set any additional attributes
        for key, value in story_dict.items():
            if not hasattr(story, key) and key != "subStories":  # Skip subStories as we've already handled it
                setattr(story, key, value)

        return story

    def getCombinedSubStoryContext(self):
        # Flatten all sub-stories from all keys in the dictionary and join their contexts
        contexts = [self.title]
        for sub_stories_list in self.subStories.values():
            for sub_story in sub_stories_list:
                contexts.append(sub_story.getStoryContext())
        return "\n".join(contexts)

    # NOTE: This is currently only used for testing in `testerDataSourcePlugin.py`
    def getStoryContext(self):
        return self.title

    def to_dict(self):
        return self.__dict__.copy()

    def set_attribute(self, key, value):
        """Set an arbitrary attribute on the story."""
        setattr(self, key, value)

    def __setitem__(self, key, value):
        """Allow dictionary-style setting of attributes."""
        self.set_attribute(key, value)

        contexts = []
        for sub_stories_list in self.subStories.values():
            for sub_story in sub_stories_list:
                contexts.append(sub_story.getStoryContext())
        return "\n".join(contexts)
