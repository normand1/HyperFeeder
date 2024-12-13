from abc import ABC, abstractmethod


class AbstractSegmentWriterPlugin(ABC):
    @abstractmethod
    def writeStorySegment(self, story, segments):
        pass

    @abstractmethod
    def identify(self) -> str:
        pass

    @abstractmethod
    def writeToDisk(self, story, scrapedText, directory, fileNameLambda):
        pass

    @abstractmethod
    def doesOutputFileExist(self, story, directory, fileNameLambda) -> bool:
        pass
