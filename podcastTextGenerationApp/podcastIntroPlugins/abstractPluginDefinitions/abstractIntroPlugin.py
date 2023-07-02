from abc import ABC, abstractmethod

class AbstractIntroPlugin(ABC):
    @abstractmethod
    def writeIntro(self, topStories, podcastName, typeOfPodcast) -> str:
        pass
    @abstractmethod
    def identify(self) -> str:
        pass
    @abstractmethod
    def writeToDisk(self, introText, fileNameIntro):
        pass
    @abstractmethod
    def doesOutputFileExist(self, fileNameIntro) -> bool:
        pass