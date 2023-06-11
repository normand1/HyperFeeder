from abc import ABC, abstractmethod

class AbstractStorySummaryPlugin(ABC):
    @abstractmethod
    def summarizeText(self, topStories, summaryTextDirNameLambda, summaryTextFileNameLambda):
        pass
    @abstractmethod
    def identify(self) -> str:
        pass