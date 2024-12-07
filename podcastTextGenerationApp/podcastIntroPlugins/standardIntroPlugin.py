from podcastIntroPlugins.baseIntroPlugin import BaseIntroPlugin
from podcastIntroPlugins.utilities.podcastIntroWriter import PodcastIntroWriter
from podcastDataSourcePlugins.models.story import Story


class StandardIntroPlugin(BaseIntroPlugin):
    def identify(self) -> str:
        return "🎹 Standard Intro Plugin"

    def writeIntro(self, stories: list[Story], podcastName: str, typeOfPodcast: str) -> str:
        if not stories or not isinstance(stories, list):
            raise ValueError("Stories must be a non-empty list.")
        if not all(isinstance(story, Story) for story in stories):
            raise ValueError("Each story must be a Story object.")

        if not isinstance(podcastName, str) or not podcastName.strip():
            raise ValueError("Podcast name must be a non-empty string.")
        if not isinstance(typeOfPodcast, str) or not typeOfPodcast.strip():
            raise ValueError("Type of podcast must be a non-empty string.")

        storyTitles = list(map(lambda story: story.title, stories))
        introText = PodcastIntroWriter().writeIntro(storyTitles, podcastName, typeOfPodcast)
        return introText


plugin = StandardIntroPlugin()
