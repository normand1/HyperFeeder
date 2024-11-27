from podcastDataSourcePlugins.models.story import Story


class PodcastStory(Story):
    def __init__(
        self,
        itemOrder: int,
        title: str,
        link: str,
        source: str,
        podcastEpisodeLink: str,
        uniqueId: str,
        rootLink: str = None,
        pubDate: str = None,
    ):
        super().__init__(itemOrder, title, link, "Podcast", uniqueId, source)
        self.itemOrder = itemOrder
        self.podcastEpisodeLink = podcastEpisodeLink
        self.uniqueId = uniqueId
        self.rootLink = rootLink
        self.pubDate = pubDate

    def to_dict(self):
        return {
            "itemOrder": self.itemOrder,
            "newsRank": self.newsRank,
            "title": self.title,
            "link": self.link,
            "storyType": self.storyType,
            "source": self.source,
            "podcastEpisodeLink": self.podcastEpisodeLink,
            "uniqueId": self.uniqueId,
            "rootLink": self.rootLink,
            "pubDate": self.pubDate,
        }
