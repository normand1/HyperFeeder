# In redditStory.py file

class RedditStory:
    def __init__(self, newsRank: int, title: str, link: str, storyType: str, source: str):
        self.newsRank = newsRank
        self.title = title
        self.link = link
        self.storyType = storyType
        self.source = source

    def to_dict(self):
        return {
            "newsRank": self.newsRank,
            "title": self.title,
            "link": self.link,
            "storyType": self.storyType,
            "source": self.source
        }