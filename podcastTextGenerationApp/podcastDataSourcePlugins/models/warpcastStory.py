from podcastDataSourcePlugins.models.story import Story


class WarpcastStory(Story):
    @classmethod
    def from_dict(cls, story_dict):
        """Create a WarpcastStory instance from a dictionary"""
        return cls(
            title=story_dict.get("text"),  # Using cast text as title
            url=story_dict.get("url"),
            content=story_dict.get("content"),
            timestamp=story_dict.get("timestamp"),
            uniqueId=story_dict.get("hash"),  # Using cast hash as unique identifier
        )

    def getStoryContext(self):
        return self.content

    def __init__(self, title, url, content, timestamp, uniqueId):
        super().__init__(0, title, url, "cast", uniqueId, "warpcast")
        self.title = title
        self.url = url
        self.content = content
        self.timestamp = timestamp

        # Fields we don't want to include when generating the podcast segment
        self.keysToIgnoreForWritingSegment.extend(["timestamp", "uniqueId"])

    def __json__(self, depth=10):
        """Make the class directly JSON serializable"""
        return {
            "title": str(self.title),
            "url": str(self.url),
            "content": str(self.content),
            "timestamp": str(self.timestamp),
            "storyType": "cast",
            "uniqueId": str(self.uniqueId),
            "source": "warpcast",
        }
