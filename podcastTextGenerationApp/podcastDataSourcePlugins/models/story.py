class Story:
    def __init__(self, newsRank, title, link, storyType, uniqueId, source):
        self.newsRank = newsRank
        self.title = title
        self.link = link
        self.storyType = storyType
        self.source = source
        self.uniqueId = uniqueId
        # This is a property that can be added to by any plugins that process this story to ignore certain keys when writing a segment for a story.
        # The context of the Story object is passed to the LLM model as a JSON object, to include context about the story.
        # However, we don't want to include the raw content of the story itself because (for now) that would most likely exceed the
        # context window for the model.
        self.keysToIgnoreForWritingSegment = ["link", "rawSplitText"]

    def to_dict(self):
        return self.__dict__
