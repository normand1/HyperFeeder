from abc import ABC, abstractmethod


class AbstractStoryScraperPlugin(ABC):
    @abstractmethod
    def scrapeSiteForText(self, story, storiesDirName):
        pass

    @abstractmethod
    def identify(self) -> str:
        pass

    @abstractmethod
    def writeToDisk(self, story, scrapedText, storiesDirName, storyFileNameLambda):
        pass

    @abstractmethod
    def doesOutputFileExist(self, story, storiesDirName, storyFileNameLambda) -> bool:
        pass

    @abstractmethod
    def doesHandleStory(self, story) -> bool:
        pass

    @abstractmethod
    def scrapeResearchAndOrganizeForSegmentWriter(self, story, storiesDirName, researchDirectoryName):
        pass
