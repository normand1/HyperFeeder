from podcastDataSourcePlugins.models.story import Story


class RSSItemStory(Story):
    @classmethod
    def from_dict(cls, story_dict):
        """Create an RSSItemStory instance from a dictionary"""
        if story_dict.get("storyType") != "RSS":
            return None

        return cls(
            itemOrder=story_dict.get("itemOrder", 0),
            title=story_dict.get("title", ""),
            link=story_dict.get("link", ""),
            content=story_dict.get("content", ""),
            raw_content=story_dict.get("raw_content"),
            rssItem=story_dict.get("rssItem", ""),
            uniqueId=story_dict.get("uniqueId", ""),
            rootLink=story_dict.get("rootLink", ""),
            pubDate=story_dict.get("pubDate", ""),
            newsRank=story_dict.get("newsRank", 0),
        )

    def getStoryContext(self):
        return self.content

    def __init__(
        self,
        itemOrder: int,
        title: str,
        link: str,
        content: str,
        raw_content: str,
        rssItem: str,
        uniqueId: str,
        rootLink: str,
        pubDate: str,
        newsRank: int,
    ):
        super().__init__(itemOrder, title, link, "RSS", uniqueId, "RSS")
        self.itemOrder = itemOrder
        self.uniqueId = uniqueId
        self.rssItem = rssItem
        self.rootLink = rootLink
        self.pubDate = pubDate
        self.newsRank = newsRank
        self.content = content
        self.raw_content = raw_content
        self.keysToIgnoreForWritingSegment.extend(["rssItem", "rootLink", "pubDate", "raw_content", "uniqueId"])

    def __json__(self, depth=10):
        """Make the class directly JSON serializable"""
        return {
            "itemOrder": self.itemOrder,
            "newsRank": self.newsRank,
            "title": str(self.title),
            "link": str(self.link),
            "content": str(self.content),
            "raw_content": self.raw_content,
            "storyType": "RSS",
            "source": "RSS",
            "uniqueId": str(self.uniqueId),
            "rssItem": self.rssItem,
            "rootLink": str(self.rootLink),
            "pubDate": str(self.pubDate),
        }
