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
            storyType=story_dict.get("storyType", "Arxiv"),
            uniqueId=story_dict.get("uniqueId", ""),
            source=story_dict.get("source", "Arxiv"),
        )

    def __init__(self, newsRank, title, link, storyType, uniqueId, source="Arxiv"):
        super().__init__(newsRank, title, link, "Arxiv", uniqueId, source)
        self.keysToIgnoreForWritingSegment.append("rawContent")
        self.hackerNewsRank = newsRank  # This gives more context to the fact that this is a hacker news article for the LLM
