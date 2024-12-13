import os
import random
import string
from datetime import datetime
from podcastDataSourcePlugins.models.story import Story
from urllib.parse import urlparse
from dotenv import load_dotenv
from podcastResearcherPlugins.abstractPluginDefinitions.abstractResearcherPlugin import AbstractResearcherPlugin
from SQLiteManager import SQLiteManager

from json_utils import dump_json


class BaseResearcherPlugin(AbstractResearcherPlugin):
    # Lower numbers run first (higher priority)
    priority = 100  # Default priority

    def __init__(self):
        currentFile = os.path.realpath(__file__)
        currentDirectory = os.path.dirname(currentFile)
        load_dotenv(os.path.join(currentDirectory, ".env.datasource"))

        self.sqlite_manager = SQLiteManager()

    def researchStories(self, segments: list[Story], researchDirName: str):
        raise NotImplementedError("researchStories() not implemented, make sure to override it in your plugin")

    def updateStories(self, segments: list[Story]):
        raise NotImplementedError("updateStories() not implemented, make sure to override it in your plugin")

    def identify(self, simpleName=False) -> str:
        raise NotImplementedError("identify() not implemented, make sure to override it in your plugin")

    def writePodcastDetails(self, podcastName, segments):
        raise NotImplementedError("writePodcastDetails() not implemented, make sure to override it in your plugin")

    def writeToDisk(self, story: Story, storiesDirName, storyFileNameLambda):
        url = story.link
        uniqueId = story.uniqueId
        rawTextFileName = storyFileNameLambda(uniqueId, url)
        filePath = os.path.join(storiesDirName, rawTextFileName)
        os.makedirs(storiesDirName, exist_ok=True)
        with open(filePath, "w", encoding="utf-8") as file:
            dump_json(story, file)
            file.flush()

    def writeResearchToDisk(self, segments: list[Story], research: dict[str, dict], researchDirName, researchFileNameLambda):
        for story in segments:
            researchForStory = research[story.uniqueId]
            # Create story-specific subdirectory
            storyDir = os.path.join(researchDirName, story.uniqueId)
            rawTextFileName = researchFileNameLambda(story.uniqueId, story.link, self.identify(simpleName=True))
            filePath = os.path.join(storyDir, rawTextFileName)
            os.makedirs(storyDir, exist_ok=True)  # Create story subdirectory
            with open(filePath, "w", encoding="utf-8") as file:
                dump_json(researchForStory, file)
                file.flush()

    @classmethod
    def makeUniqueStoryIdentifier(cls) -> str:
        characters = string.ascii_uppercase + string.ascii_lowercase + string.digits
        randomId = "".join(random.choice(characters) for _ in range(6))
        return randomId

    def doesOutputFileExist(self, story: Story, storiesDirName, storyFileNameLambda) -> bool:
        url = story.link
        uniqueId = story.uniqueId
        rawTextFileName = storyFileNameLambda(uniqueId, url)
        filePath = os.path.join(storiesDirName, rawTextFileName)
        if os.path.exists(filePath):
            print("Story file already exists at filepath: " + filePath + ", skipping scraping story")
            return True
        else:
            return False

    def url_to_filename(self, url):
        parts = urlparse(url)
        filename = parts.netloc + parts.path
        filename = filename.replace("/", "_")  # Replace slashes with underscores
        filename = filename.replace(":", "_")  # Replace colons with underscores
        filename = filename.replace("-", "_")  # Replace dashes with underscores
        return filename

    def parseDate(self, dateString):
        dateFormats = ["%a, %d %b %Y %H:%M:%S %Z", "%a, %d %b %Y %H:%M:%S %z"]
        for fmt in dateFormats:
            try:
                return datetime.strptime(dateString, fmt)
            except ValueError:
                pass
        raise ValueError(f"time data '{dateString}' does not match any format")
