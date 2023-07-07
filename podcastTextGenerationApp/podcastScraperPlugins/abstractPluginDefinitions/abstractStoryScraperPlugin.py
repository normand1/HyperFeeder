from abc import ABC, abstractmethod


class AbstractStoryScraperPlugin(ABC):
    @abstractmethod
    def scrapeSiteForText(self, story):
        pass

    @abstractmethod
    def identify(self) -> str:
        pass

    @abstractmethod
    def writeToDisk(self, story, rawTextDirNameLambda, rawTextFileNameLambda):
        pass

    @abstractmethod
    def doesOutputFileExist(self, rawTextDirNameLambda, rawTextFileNameLambda) -> bool:
        pass
