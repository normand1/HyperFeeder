from story import Story
from abc import ABC, abstractmethod
from typing import List

class AbstractDataSourcePlugin(ABC):
    @abstractmethod
    def fetchStories(self) -> List[Story]:
        pass
    @abstractmethod
    def identify(self) -> str:
        pass