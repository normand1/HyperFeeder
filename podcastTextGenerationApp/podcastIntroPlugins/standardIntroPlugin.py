from podcastIntroPlugins.baseIntroPlugin import BaseIntroPlugin
from podcastIntroPlugins.utilities.podcastIntroWriter import PodcastIntroWriter
from podcastDataSourcePlugins.models.segment import Segment


class StandardIntroPlugin(BaseIntroPlugin):
    def identify(self) -> str:
        return "🎹 Standard Intro Plugin"

    def writeIntro(self, segments: list[Segment], podcastName: str, typeOfPodcast: str) -> str:
        if not segments or not isinstance(segments, list):
            raise ValueError("Stories must be a non-empty list.")
        if not all(isinstance(story, Segment) for story in segments):
            raise ValueError("Each story must be a Segment object.")

        if not isinstance(podcastName, str) or not podcastName.strip():
            raise ValueError("Podcast name must be a non-empty string.")
        if not isinstance(typeOfPodcast, str) or not typeOfPodcast.strip():
            raise ValueError("Type of podcast must be a non-empty string.")

        combinedStorySegments = list(map(lambda story: story.rawSplitText, segments))
        introText = PodcastIntroWriter().writeIntro(combinedStorySegments, podcastName, typeOfPodcast)
        return introText


plugin = StandardIntroPlugin()
