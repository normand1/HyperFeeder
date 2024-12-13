import json
import os
from abc import abstractmethod

from dotenv import load_dotenv
from podcastOutroWriterPlugins.abstractPluginDefinitions.abstractOutroPlugin import (
    AbstractOutroPlugin,
)


class BaseOutroWriterPlugin(AbstractOutroPlugin):
    def __init__(self):
        currentFile = os.path.realpath(__file__)
        currentDirectory = os.path.dirname(currentFile)
        load_dotenv(os.path.join(currentDirectory, ".env.outro"))

    @abstractmethod
    def writeOutro(self, segments, introText):
        pass

    @abstractmethod
    def identify(self) -> str:
        pass

    def writeToDisk(self, outroText, outroTextDirName):
        directory = os.path.dirname(outroTextDirName)
        os.makedirs(directory, exist_ok=True)
        with open(outroTextDirName, "w", encoding="utf-8") as file:
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
