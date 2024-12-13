from abc import ABC, abstractmethod


class AbstractOutroPlugin(ABC):
    @abstractmethod
    def writeOutro(self, segments, introText):
        pass

    @abstractmethod
    def identify(self) -> str:
        pass

    @abstractmethod
    def writeToDisk(self, outroText, outroTextDirName):
        pass
