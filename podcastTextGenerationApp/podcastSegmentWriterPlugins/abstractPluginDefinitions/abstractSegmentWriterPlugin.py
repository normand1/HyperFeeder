from abc import ABC, abstractmethod

class AbstractSegmentWriterPlugin(ABC):
    @abstractmethod
    def writeStorySegment(self, topStories, segmentTextDirNameLambda, segmemntTextFileNameLambda):
        pass
    @abstractmethod
    def identify(self) -> str:
        pass