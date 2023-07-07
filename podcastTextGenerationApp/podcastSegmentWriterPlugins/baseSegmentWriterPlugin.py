from abc import abstractmethod
import os, json
from podcastSegmentWriterPlugins.abstractPluginDefinitions.abstractSegmentWriterPlugin import (
    AbstractSegmentWriterPlugin,
)
from dotenv import load_dotenv


class BaseSegmentWriterPlugin(AbstractSegmentWriterPlugin):
    def __init__(self):
        currentFile = os.path.realpath(__file__)
        currentDirectory = os.path.dirname(currentFile)
        load_dotenv(os.path.join(currentDirectory, ".env.writer"))

    @abstractmethod
    def writeStorySegment(self, story):
        pass

    @abstractmethod
    def identify(self) -> str:
        pass

    def writeToDisk(self, story, scrapedText, directory, fileNameLambda):
        url = story["link"]
        uniqueId = story["uniqueId"]
        filename = fileNameLambda(uniqueId, url)
        filePath = os.path.join(directory, filename)
        os.makedirs(directory, exist_ok=True)
        with open(filePath, "w") as file:
            json.dump(scrapedText, file)
            file.flush()

    def doesOutputFileExist(self, story, directory, fileNameLambda) -> bool:
        url = story["link"]
        uniqueId = story["uniqueId"]
        filename = fileNameLambda(uniqueId, url)
        filePath = os.path.join(directory, filename)
        numberedFilePath = os.path.join(directory, f"{story['newsRank']+1}_{filename}")
        if os.path.exists(filePath) or os.path.exists(numberedFilePath):
            print(
                "Segment text file already exists at filepath: "
                + filePath
                + ", skipping writing segment for story"
            )
            return True
        else:
            return False

    def cleanupStorySummary(self, story) -> str:
        summaryText = story
        summaryText = summaryText.replace("\\", "")
        summaryText = summaryText.replace("   ", "")
        summaryText = summaryText.replace("  ", "")
        return summaryText
