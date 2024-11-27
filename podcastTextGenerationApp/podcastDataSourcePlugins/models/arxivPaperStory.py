from podcastDataSourcePlugins.models.story import Story


class ArxivPaperStory(Story):
    def __init__(self, newsRank, title, link, storyType, uniqueId, source="Arxiv"):
        super().__init__(newsRank, title, link, storyType, uniqueId, source)
        self.keysToIgnoreForWritingSegment.append("rawContent")
        self.hackerNewsRank = newsRank  # This gives more context to the fact that this is a hacker news article for the LLM
