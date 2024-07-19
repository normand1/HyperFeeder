class Story:
    def __init__(self, newsRank, title, link, storyType, uniqueId, source):
        self.newsRank = newsRank
        self.title = title
        self.link = link
        self.storyType = storyType
        self.source = source
        self.uniqueId = uniqueId
        self.keysToIgnoreForWritingSegment = [
            "link",
        ]

    def to_dict(self):
        return self.__dict__
