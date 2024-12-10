from abc import ABC, abstractmethod


class AbstractProducerPlugin(ABC):
    @abstractmethod
    def updateFileNames(
        self,
        segments,
        outroTextDirName,
        introDirName,
        segmentTextDirNameLambda,
        fileNameLambda,
    ):
        pass

    @abstractmethod
    def identify(self) -> str:
        pass

    @abstractmethod
    def renameFile(self, directory, oldName, newName):
        pass

    @abstractmethod
    def orderStories(self, segments):
        pass
