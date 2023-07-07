from podcastIntroPlugins.baseIntroPlugin import BaseIntroPlugin


class TesterIntroPlugin(BaseIntroPlugin):
    def identify(self) -> str:
        return "Tester Intro Plugin"

    def writeIntro(self, topStories, podcastName, typeOfPodcast) -> str:
        return "test intro text"


plugin = TesterIntroPlugin()
