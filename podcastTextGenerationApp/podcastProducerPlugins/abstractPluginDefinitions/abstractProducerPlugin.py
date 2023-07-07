from abc import ABC, abstractmethod


class AbstractProducerPlugin(ABC):
    @abstractmethod
    def updateFileNames(
        self,
        stories,
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
