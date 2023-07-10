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
    ):
        super().__init__(itemOrder, title, link, storyType, uniqueId, source)
        self.itemOrder = itemOrder
        self.uniqueId = uniqueId
        self.rssItem = rssItem
        self.rootLink = rootLink
        self.pubDate = pubDate
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
