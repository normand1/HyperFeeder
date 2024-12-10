from podcastDataSourcePlugins.models.story import Story


class TavilyStory(Story):
    @classmethod
    def from_dict(cls, story_dict):
        """Create a TavilyStory instance from a dictionary"""

        return cls(
            title=story_dict.get("title"),
            url=story_dict.get("url"),
            content=story_dict.get("content"),
            score=story_dict.get("score", 0.0),
            raw_content=story_dict.get("raw_content"),
            uniqueId=story_dict.get("url"),  # Using URL as the unique identifier
        )

    def getStoryContext(self):
        return self.content

    def __init__(self, title, url, content, score, raw_content, uniqueId):
        super().__init__(0, title, url, "article", uniqueId, "tavily")
        self.title = title
        self.url = url
        self.content = content
        self.score = score
        self.raw_content = raw_content
        self.keysToIgnoreForWritingSegment.append("raw_content")
        self.keysToIgnoreForWritingSegment.append("score")
        self.keysToIgnoreForWritingSegment.append("uniqueId")

    def __json__(self, depth=10):
        """Make the class directly JSON serializable"""
        return {
            "title": str(self.title),
            "url": str(self.url),
            "content": str(self.content),
            "score": float(self.score),
            "raw_content": self.raw_content,
            "storyType": "article",
            "uniqueId": str(self.uniqueId),
            "source": "tavily",
        }
