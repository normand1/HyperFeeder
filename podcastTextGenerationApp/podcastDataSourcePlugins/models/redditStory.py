class RedditStory:
    def __init__(self, newsRank: int, title: str, link: str, storyType: str, source: str, uniqueId: str):
        self.newsRank = newsRank
        self.title = title
        self.link = link
        self.storyType = storyType
        self.source = source
        self.uniqueId = uniqueId

    def to_dict(self):
        return {
            "newsRank": self.newsRank,
            "title": self.title,
            "link": self.link,
            "storyType": self.storyType,
            "source": self.source,
            "uniqueId": self.uniqueId
        }