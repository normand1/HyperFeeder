from podcastIntroPlugins.baseIntroPlugin import BaseIntroPlugin
from podcastIntroPlugins.utilities.podcastIntroWriter import PodcastIntroWriter


class StandardIntroPlugin(BaseIntroPlugin):
    def identify(self) -> str:
        return "🎹 Standard Intro Plugin"

    def writeIntro(self, stories, podcastName, typeOfPodcast) -> str:
        storyTitles = list(map(lambda story: story["title"], stories))
        introText = PodcastIntroWriter().writeIntro(
            storyTitles, podcastName, typeOfPodcast
        )
        return introText


plugin = StandardIntroPlugin()
