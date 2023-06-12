class PodcastStory:
    def __init__(self, podcastOrder: int, title: str, link: str, storyType: str, source: str, podcastEpisodeLink: str):
        self.podcastOrder = podcastOrder
        self.title = title
        self.link = link
        self.storyType = storyType
        self.source = source
        self.podcastEpisodeLink = podcastEpisodeLink

    def to_dict(self):
        return {
            "podcastOrder": self.podcastOrder,
            "title": self.title,
            "link": self.link,
            "storyType": self.storyType,
            "source": self.source,
            "podcastEpisodeLink": self.podcastEpisodeLink
        }