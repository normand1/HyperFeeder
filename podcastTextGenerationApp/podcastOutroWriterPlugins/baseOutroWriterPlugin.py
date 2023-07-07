from abc import abstractmethod
import os, json
from podcastOutroWriterPlugins.abstractPluginDefinitions.abstractOutroPlugin import AbstractOutroPlugin
from dotenv import load_dotenv

class BaseOutroWriterPlugin(AbstractOutroPlugin):
    def __init__(self):
        currentFile = os.path.realpath(__file__)
        currentDirectory = os.path.dirname(currentFile)
        load_dotenv(os.path.join(currentDirectory, '.env.outro'))
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
    