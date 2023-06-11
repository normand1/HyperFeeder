import os
from podcastIntroPlugins.abstractPluginDefinitions.abstractIntroPlugin import AbstractIntroPlugin
from podcastIntroWriter import PodcastIntroWriter

class StandardIntroPlugin(AbstractIntroPlugin):

    def identify(self) -> str:
        return "📑 Standard Intro Plugin"

    def writeIntro(self, topStories, podcastName, fileNameIntro, typeOfPodcast):
        storyTitles = list(map(lambda story: story["title"], topStories[1:]))
        self.writeIntroSegment(storyTitles, podcastName, fileNameIntro, typeOfPodcast)

    
    def writeIntroSegment(self, storyTitles, podcastName, fileNameIntro, typeOfPodcast):
        if not os.path.isfile(fileNameIntro):
            directory = os.path.dirname(fileNameIntro)
            os.makedirs(directory, exist_ok=True)
            with open(fileNameIntro, 'w') as file:
                introText = PodcastIntroWriter().writeIntro(storyTitles, podcastName, typeOfPodcast)
                file.write(introText)
        else:
            print("intro file already exists, skipping writing intro")

plugin = StandardIntroPlugin()