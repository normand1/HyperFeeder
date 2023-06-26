from abc import ABC, abstractmethod

class AbstractStorySummaryPlugin(ABC):
    @abstractmethod
    def summarizeText(self, story):
        pass
    @abstractmethod
    def identify(self) -> str:
        pass
    @abstractmethod
    def writeToDisk(self, story, summaryText, summaryTextDirName, summaryTextFileNameLambda):
        pass
    @abstractmethod
    def doesOutputFileExist(self, story, summaryTextDirName, summaryTextFileNameLambda) -> bool:
        pass