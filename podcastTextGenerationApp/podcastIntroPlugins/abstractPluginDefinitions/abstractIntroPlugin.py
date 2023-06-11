from story import Story
from abc import ABC, abstractmethod

class AbstractIntroPlugin(ABC):
    @abstractmethod
    def writeIntro(self, topStories, podcastName, fileNameIntro, typeOfPodcast):
        pass
    @abstractmethod
    def identify(self) -> str:
        pass