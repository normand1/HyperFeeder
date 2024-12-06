from abc import ABC, abstractmethod
from podcastDataSourcePlugins.models.story import Story


# This is the abstract class for the researcher plugins
# These plugins are used to research the stories and add additional information to story object models
class AbstractResearcherPlugin(ABC):
    @abstractmethod
    def updateStories(self, stories: list[Story]) -> list[Story]:
        pass

    @abstractmethod
    def researchStories(self, stories: list[Story], researchDirName: str):
        pass

    @abstractmethod
    def identify(self, simpleName=False) -> str:
        pass

    @abstractmethod
    def writeToDisk(self, story, storiesDirName, storyFileNameLambda):
        pass
