from podcastDataSourcePlugins.models.story import Story

class PodcastStory(Story):
    def __init__(self, podcastOrder: int, title: str, link: str, storyType: str, source: str, podcastEpisodeLink: str, uniqueId: str):
        super().__init__(podcastOrder, title, link, storyType, uniqueId, source)
        self.podcastOrder = podcastOrder
        self.podcastEpisodeLink = podcastEpisodeLink
        self.uniqueId = uniqueId
        self.keysToIgnoreForWritingSegment.append("rawContent")
    def to_dict(self):
        return {
            "podcastOrder": self.podcastOrder,
            "newsRank": self.newsRank,
            "title": self.title,
            "link": self.link,
            "storyType": self.storyType,
            "source": self.source,
            "podcastEpisodeLink": self.podcastEpisodeLink,
            "uniqueId": self.uniqueId
        }