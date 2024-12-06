class Story:
    def __init__(self, newsRank, title, link, storyType, uniqueId, source):
        self.newsRank = newsRank
        self.title = title
        self.link = link
        self.storyType = storyType
        self.source = source
        self.uniqueId = uniqueId
        self.keysToIgnoreForWritingSegment = [
            "link",
        ]

    def __json__(self):
        """Make the class directly JSON serializable"""
        return {"newsRank": self.newsRank, "title": self.title, "link": self.link, "storyType": self.storyType, "source": self.source, "uniqueId": self.uniqueId}

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
            return story_class.from_dict(story_dict)

        # If no specific type or unknown type, create base Story
        story = cls(
            newsRank=story_dict.get("newsRank", 0),
            title=story_dict.get("title", ""),
            link=story_dict.get("link", ""),
            storyType=story_dict.get("storyType", "Unknown"),
            uniqueId=story_dict.get("uniqueId", ""),
            source=story_dict.get("source", "Unknown"),
        )

        # Set any additional attributes
        for key, value in story_dict.items():
            if not hasattr(story, key):
                setattr(story, key, value)

        return story

    def to_dict(self):
        return self.__dict__.copy()

    def set_attribute(self, key, value):
        """Set an arbitrary attribute on the story."""
        setattr(self, key, value)

    def __setitem__(self, key, value):
        """Allow dictionary-style setting of attributes."""
        self.set_attribute(key, value)
