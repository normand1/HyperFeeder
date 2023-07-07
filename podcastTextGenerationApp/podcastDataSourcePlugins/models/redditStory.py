from podcastDataSourcePlugins.models.story import Story


class RedditStory(Story):
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
