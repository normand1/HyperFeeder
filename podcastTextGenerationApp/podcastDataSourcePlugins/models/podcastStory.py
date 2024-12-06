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

    @classmethod
    def from_dict(cls, story_dict):
        """Create a PodcastStory instance from a dictionary"""
        if story_dict.get("storyType") != "Podcast":
            return None

        return cls(
            itemOrder=story_dict.get("itemOrder", 0),
            title=story_dict.get("title", ""),
            link=story_dict.get("link", ""),
            source=story_dict.get("source", "Unknown"),
            podcastEpisodeLink=story_dict.get("podcastEpisodeLink", ""),
            uniqueId=story_dict.get("uniqueId", ""),
            rootLink=story_dict.get("rootLink"),
            pubDate=story_dict.get("pubDate"),
        )
