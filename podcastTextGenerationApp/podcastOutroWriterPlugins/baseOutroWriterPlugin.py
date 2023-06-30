from abc import abstractmethod
import os, json
from podcastOutroWriterPlugins.abstractPluginDefinitions.abstractOutroPlugin import AbstractOutroPlugin

class BaseOutroWriterPlugin(AbstractOutroPlugin):
    @abstractmethod
    def writeOutro(self, story):
        pass
    @abstractmethod
    def identify(self) -> str:
        pass
    def writeToDisk(self, outroText, outroTextDirName):
        directory = os.path.dirname(outroTextDirName)
        os.makedirs(directory, exist_ok=True)
        with open(outroTextDirName, 'w') as file:
            json.dump(outroText, file)
            file.flush()
    def doesOutputFileExist(self, outroTextDirName):
        return os.path.isfile(outroTextDirName)
    def cleanupStorySummary(self, story) -> str:
        summaryText = story
        summaryText = summaryText.replace("\\", "")
        summaryText = summaryText.replace("   ", "")
        summaryText = summaryText.replace("  ", "")
        return summaryText
    