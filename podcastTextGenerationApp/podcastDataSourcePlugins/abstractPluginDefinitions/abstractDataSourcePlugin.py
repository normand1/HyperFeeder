from podcastDataSourcePlugins.models.story import Story
from abc import ABC, abstractmethod
from typing import List


class AbstractDataSourcePlugin(ABC):
    @abstractmethod
    def fetchStories(self) -> List[Story]:
        pass

    @abstractmethod
    def identify(self) -> str:
        pass

    @abstractmethod
    def writePodcastDetails(self, podcastName, stories):
        pass

    @abstractmethod
    def writeToDisk(self, story, storiesDirName, storyFileNameLambda):
        pass

    @abstractmethod
    def makeUniqueStoryIdentifier(self) -> str:
        pass
