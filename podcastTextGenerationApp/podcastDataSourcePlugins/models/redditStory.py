from podcastDataSourcePlugins.models.story import Story


class RedditStory(Story):
    @classmethod
    def from_dict(cls, story_dict):
        """Create a RedditStory instance from a dictionary"""
        if story_dict.get("storyType") != "Reddit":
            return None

        return cls(
            newsRank=story_dict.get("newsRank", 0),
            title=story_dict.get("title", ""),
            link=story_dict.get("link", ""),
            storyType=story_dict.get("storyType", "Reddit"),
            uniqueId=story_dict.get("uniqueId", ""),
            source=story_dict.get("source", "Reddit"),
        )

    def __init__(
        self,
        newsRank: int,
        title: str,
        link: str,
        storyType: str,
        uniqueId: str,
        source="Reddit",
    ):
        super().__init__(newsRank, title, link, storyType, uniqueId, source)
        self.keysToIgnoreForWritingSegment.append("rawContent")

    def to_dict(self):
        return {
            "newsRank": self.newsRank,
            "title": self.title,
            "link": self.link,
            "storyType": self.storyType,
            "uniqueId": self.uniqueId,
            "source": self.source,
            "keysToIgnoreForWritingSegment": self.keysToIgnoreForWritingSegment,
        }
