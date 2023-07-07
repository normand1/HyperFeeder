from abc import ABC, abstractmethod


class AbstractProducerPlugin(ABC):
    @abstractmethod
    def updateFileNames(
        self, stories, outroTextDirName, introDirName, segmentTextDirNameLambda
    ):
        pass

    @abstractmethod
    def identify(self) -> str:
        pass

    @abstractmethod
    def rename_file(directory, old_name, new_name):
        pass
