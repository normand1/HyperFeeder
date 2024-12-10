from podcastDataSourcePlugins.models.story import Story
from abc import ABC, abstractmethod
from typing import List


class AbstractDataSourcePlugin(ABC):

    @classmethod
    @abstractmethod
    def identify(cls, simpleName=False) -> str:
        pass

    @abstractmethod
    def writePodcastDetails(self, podcastName, stories):
        pass

    @staticmethod
    @abstractmethod
    def writeToDisk(story, storiesDirName, storyFileNameLambda):
        pass

    @classmethod
    @abstractmethod
    def makeUniqueStoryIdentifier(cls) -> str:
        pass

    @abstractmethod
    def getTools(self):
        pass

    @abstractmethod
    def filterForImportantContextOnly(self, subStoryContent: dict):
        pass

    @abstractmethod
    def fetchContentForStory(self, story: Story):
        pass
