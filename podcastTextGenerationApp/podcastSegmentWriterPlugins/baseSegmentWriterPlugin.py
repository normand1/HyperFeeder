from abc import abstractmethod
import os, json
from podcastDataSourcePlugins.baseDataSourcePlugin import Story
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
    def writeStorySegment(self, story, stories):
        pass

    @abstractmethod
    def identify(self) -> str:
        pass

    def writeToDisk(self, story: Story, scrapedText, directory, fileNameLambda):
        uuid = story.uniqueId
        filename = fileNameLambda(uuid)
        filePath = os.path.join(directory, filename)
        os.makedirs(directory, exist_ok=True)
        with open(filePath, "w", encoding="utf-8") as file:
            json.dump(scrapedText, file)
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

    def cleanupStorySummary(self, story) -> str:
        summaryText = story
        summaryText = summaryText.replace("\\", "")
        summaryText = summaryText.replace("   ", "")
        summaryText = summaryText.replace("  ", "")
        return summaryText

    def cleanText(self, text: str) -> str:
        """
        Cleans up the input text by removing or replacing unwanted characters and formatting.

        Parameters:
        - text (str): The text to be cleaned.

        Returns:
        - str: The cleaned text.
        """

        # 1. Decode unicode escape sequences to actual characters
        try:
            text = codecs.decode(text, "unicode_escape")
        except Exception:
            # If decoding fails, keep the original text
            pass

        # 2. Replace escaped single and double quotes with actual quotes
        text = text.replace("\\'", "'").replace('\\"', '"')

        # 3. Remove other common escape sequences (e.g., backslashes, tabs)
        escape_sequences = {
            r"\\": "\\",  # Replace double backslashes with a single backslash
            r"\n": " ",  # Replace newline characters with a space
            r"\t": " ",  # Replace tab characters with a space
            r"\r": " ",  # Replace carriage returns with a space
            # Add more escape sequences if necessary
        }
        for esc, char in escape_sequences.items():
            text = text.replace(esc, char)

        # 4. Remove asterisks used for bold or italic markdown formatting
        text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)  # Remove **bold**
        text = re.sub(r"\*(.*?)\*", r"\1", text)  # Remove *italic*

        # 5. Remove numbers with periods used for list formatting (e.g., "1. Item")
        text = re.sub(r"^\d+\.\s+", "", text, flags=re.MULTILINE)

        # 6. Remove markdown links but keep the link text
        text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)

        # 7. Remove markdown images
        text = re.sub(r"!\[([^\]]*)\]\([^\)]+\)", "", text)

        # 8. Remove HTML tags if any
        text = re.sub(r"<[^>]+>", "", text)

        # 9. Remove inline code snippets enclosed in backticks
        text = re.sub(r"`{1,3}[^`]*`{1,3}", "", text)

        # 10. Replace multiple whitespace characters with a single space
        text = re.sub(r"\s+", " ", text)

        # 11. Strip leading and trailing whitespace
        text = text.strip()

        return text
