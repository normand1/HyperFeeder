from abc import abstractmethod
import os, json
from podcastDataSourcePlugins.baseDataSourcePlugin import Story
from podcastSegmentWriterPlugins.abstractPluginDefinitions.abstractSegmentWriterPlugin import (
    AbstractSegmentWriterPlugin,
)
from dotenv import load_dotenv
import re


class BaseSegmentWriterPlugin(AbstractSegmentWriterPlugin):
    def __init__(self):
        currentFile = os.path.realpath(__file__)
        currentDirectory = os.path.dirname(currentFile)
        load_dotenv(os.path.join(currentDirectory, ".env.writer"))

    @abstractmethod
    def writeStorySegment(self, story, stories):
        pass

    @abstractmethod
    def identify(self) -> str:
        pass

    def writeToDisk(self, story: Story, scrapedText, directory, fileNameLambda):
        url = story.link
        uniqueId = story.uniqueId
        filename = fileNameLambda(uniqueId, url)
        filePath = os.path.join(directory, filename)
        os.makedirs(directory, exist_ok=True)
        with open(filePath, "w") as file:
            json.dump(scrapedText, file)
            file.flush()

    def doesOutputFileExist(self, story, directory, fileNameLambda) -> bool:
        url = story.link
        uniqueId = story.uniqueId
        filename = fileNameLambda(uniqueId, url)

        if not os.path.exists(directory):
            return False

        for existing_file in os.listdir(directory):
            if filename in existing_file:
                print(f"Segment text file already exists: {existing_file}, skipping writing segment for story")
                return True

        return False

    def cleanupStorySummary(self, story) -> str:
        summaryText = story
        summaryText = summaryText.replace("\\", "")
        summaryText = summaryText.replace("   ", "")
        summaryText = summaryText.replace("  ", "")
        return summaryText

    def cleanText(self, text) -> str:
        # Remove unicode escape sequences
        text = re.sub(r"\\u[0-9a-fA-F]{4}", "", text)

        # Remove newline characters
        text = text.replace("\n", " ")

        # Remove asterisks used for bold formatting
        text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)

        # Remove numbers with periods used for list formatting
        text = re.sub(r"\d+\.\s", "", text)

        # Replace multiple spaces with a single space
        text = re.sub(r"\s+", " ", text)

        # Strip leading and trailing whitespace
        text = text.strip()

        return text
