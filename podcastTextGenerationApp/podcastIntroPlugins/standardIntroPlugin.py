from podcastIntroPlugins.baseIntroPlugin import BaseIntroPlugin
from podcastIntroPlugins.utilities.podcastIntroWriter import PodcastIntroWriter


class StandardIntroPlugin(BaseIntroPlugin):
    def identify(self) -> str:
        return "🎹 Standard Intro Plugin"

    def writeIntro(self, stories: list[dict], podcastName: str, typeOfPodcast: str) -> str:
        if not stories or not isinstance(stories, list):
            raise ValueError("Stories must be a non-empty list.")
        if not all(isinstance(story, dict) and "title" in story for story in stories):
            raise ValueError("Each story must be a dictionary with a 'title' key.")

        if not isinstance(podcastName, str) or not podcastName.strip():
            raise ValueError("Podcast name must be a non-empty string.")
        if not isinstance(typeOfPodcast, str) or not typeOfPodcast.strip():
            raise ValueError("Type of podcast must be a non-empty string.")

        storyTitles = list(map(lambda story: story["title"], stories))
        introText = PodcastIntroWriter().writeIntro(storyTitles, podcastName, typeOfPodcast)

        if not isinstance(introText, dict) or "text" not in introText:
            raise ValueError("Invalid response from PodcastIntroWriter: expected dictionary with 'text' key")

        return introText["text"]


plugin = StandardIntroPlugin()
