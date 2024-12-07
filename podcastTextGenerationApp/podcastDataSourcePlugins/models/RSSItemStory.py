from podcastDataSourcePlugins.models.story import Story


class RSSItemStory(Story):
    def __init__(
        self,
        itemOrder: int,
        title: str,
        link: str,
        storyType: str,
        source: str,
        rssItem: str,
        uniqueId: str,
        rootLink: str,
        pubDate: str,
        newsRank: int,
    ):
        super().__init__(itemOrder, title, link, storyType, uniqueId, source)
        self.itemOrder = itemOrder
        self.uniqueId = uniqueId
        self.rssItem = rssItem
        self.rootLink = rootLink
        self.pubDate = pubDate
        self.newsRank = newsRank
        self.keysToIgnoreForWritingSegment.append("rssItem")
        self.keysToIgnoreForWritingSegment.append("rootLink")
        self.keysToIgnoreForWritingSegment.append("pubDate")

    def to_dict(self):
        return {
            "itemOrder": self.itemOrder,
            "newsRank": self.newsRank,
            "title": self.title,
            "link": self.link,
            "storyType": self.storyType,
            "source": self.source,
            "uniqueId": self.uniqueId,
            "rssItem": self.rssItem,
            "keysToIgnoreForWritingSegment": self.keysToIgnoreForWritingSegment,
            "rootLink": self.rootLink,
            "pubDate": self.pubDate,
        }

    @classmethod
    def from_dict(cls, story_dict):
        """Create an RSSItemStory instance from a dictionary"""
        if story_dict.get("storyType") != "RSS":
            return None

        return cls(
            itemOrder=story_dict.get("itemOrder", 0),
            title=story_dict.get("title", ""),
            link=story_dict.get("link", ""),
            storyType=story_dict.get("storyType", "RSS"),
            source=story_dict.get("source", "Unknown"),
            rssItem=story_dict.get("rssItem", ""),
            uniqueId=story_dict.get("uniqueId", ""),
            rootLink=story_dict.get("rootLink", ""),
            pubDate=story_dict.get("pubDate", ""),
            newsRank=story_dict.get("newsRank", 0),
        )
