class PodcastStory:
    def __init__(self, podcastOrder: int, title: str, link: str, storyType: str, source: str, podcastEpisodeLink: str, uniqueId: str):
        self.podcastOrder = podcastOrder
        self.newsRank = podcastOrder
        self.title = title
        self.link = link
        self.storyType = storyType
        self.source = source
        self.podcastEpisodeLink = podcastEpisodeLink
        self.uniqueId = uniqueId

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