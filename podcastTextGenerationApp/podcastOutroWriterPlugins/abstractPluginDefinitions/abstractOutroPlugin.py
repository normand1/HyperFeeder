from abc import ABC, abstractmethod

class AbstractOutroPlugin(ABC):
    @abstractmethod
    def writeOutro(self, topStories):
        pass
    @abstractmethod
    def identify(self) -> str:
        pass
    @abstractmethod
    def writeToDisk(self, story, scrapedText, directory, fileNameLambda):
        pass