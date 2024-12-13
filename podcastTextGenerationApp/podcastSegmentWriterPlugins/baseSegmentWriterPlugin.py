from abc import abstractmethod
import os, json
from podcastDataSourcePlugins.models.segment import Segment
from podcastSegmentWriterPlugins.abstractPluginDefinitions.abstractSegmentWriterPlugin import (
    AbstractSegmentWriterPlugin,
)
from dotenv import load_dotenv
import re
import codecs


class BaseSegmentWriterPlugin(AbstractSegmentWriterPlugin):
    def __init__(self):
        currentFile = os.path.realpath(__file__)
        currentDirectory = os.path.dirname(currentFile)
        load_dotenv(os.path.join(currentDirectory, ".env.writer"))

    @abstractmethod
    def writeStorySegment(self, story, segments):
        pass

    @abstractmethod
    def identify(self) -> str:
        pass

    def writeToDisk(self, story: Segment, scrapedText, directory, fileNameLambda):
        uuid = story.uniqueId
        filename = fileNameLambda(uuid)
        filePath = os.path.join(directory, filename)
        os.makedirs(directory, exist_ok=True)
        with open(filePath, "w", encoding="utf-8") as file:
            file.write(scrapedText)
            file.flush()

    def doesOutputFileExist(self, story, directory, fileNameLambda) -> bool:
        uuid = story.uniqueId
        filename = fileNameLambda(uuid)

        if not os.path.exists(directory):
            return False

        for existing_file in os.listdir(directory):
            if filename in existing_file:
                print(f"Segment text file already exists: {existing_file}, skipping writing segment for story")
                return True

        return False
