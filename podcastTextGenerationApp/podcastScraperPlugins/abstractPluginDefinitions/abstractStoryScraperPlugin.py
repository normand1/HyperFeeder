from abc import ABC, abstractmethod

class AbstractStoryScraperPlugin(ABC):
    @abstractmethod
    def scrapeSitesForText(self, topStories, rawTextDirNameLambda, rawTextFileNameLambda):
        pass
    @abstractmethod
    def identify(self) -> str:
        pass
    