from podcastDataSourcePlugins.models.story import Story


class ArxivPaperStory(Story):
    @classmethod
    def from_dict(cls, story_dict):
        """Create an ArxivPaperStory instance from a dictionary"""
        if story_dict.get("storyType") != "Arxiv":
            return None

        return cls(
            newsRank=story_dict.get("newsRank", 0),
            title=story_dict.get("title", ""),
            link=story_dict.get("link", ""),
            content=story_dict.get("content", ""),
            raw_content=story_dict.get("raw_content"),
            uniqueId=story_dict.get("uniqueId", ""),
        )

    def getStoryContext(self):
        return self.content

    def __init__(
        self,
        newsRank: int,
        title: str,
        link: str,
        content: str,
        raw_content: str,
        uniqueId: str,
    ):
        super().__init__(newsRank, title, link, "Arxiv", uniqueId, "Arxiv")
        self.content = content
        self.raw_content = raw_content
        self.hackerNewsRank = newsRank  # This gives more context to the fact that this is a hacker news article for the LLM
        self.keysToIgnoreForWritingSegment.extend(["raw_content", "uniqueId"])

    def __json__(self, depth=10):
        """Make the class directly JSON serializable"""
        return {
            "newsRank": self.newsRank,
            "hackerNewsRank": self.hackerNewsRank,
            "title": str(self.title),
            "link": str(self.link),
            "content": str(self.content),
            "raw_content": self.raw_content,
            "storyType": "Arxiv",
            "uniqueId": str(self.uniqueId),
            "source": "Arxiv",
        }
