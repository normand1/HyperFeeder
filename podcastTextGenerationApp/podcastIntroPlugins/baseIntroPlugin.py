from abc import abstractmethod
import os
from podcastIntroPlugins.abstractPluginDefinitions.abstractIntroPlugin import AbstractIntroPlugin


class BaseIntroPlugin(AbstractIntroPlugin):
    @abstractmethod
    def identify(self) -> str:
        pass
    @abstractmethod
    def writeIntro(self, topStories, podcastName, typeOfPodcast) -> str:
        pass
    def writeToDisk(self, introText, fileNameIntro):    
        directory = os.path.dirname(fileNameIntro)
        os.makedirs(directory, exist_ok=True)
        with open(fileNameIntro, 'w') as file:
            file.write(introText)
    def doesOutputFileExist(self, fileNameIntro) -> bool:
        return os.path.isfile(fileNameIntro)