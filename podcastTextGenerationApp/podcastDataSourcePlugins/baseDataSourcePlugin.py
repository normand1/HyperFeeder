import json
import os
import random
import string
from datetime import datetime
from typing import List
from urllib.parse import urlparse

import firebase_admin
from dotenv import load_dotenv
from firebase_admin import credentials
from podcastDataSourcePlugins.abstractPluginDefinitions.abstractDataSourcePlugin import (
    AbstractDataSourcePlugin,
)
from podcastDataSourcePlugins.models.story import Story


class BaseDataSourcePlugin(AbstractDataSourcePlugin):
    def __init__(self):
        currentFile = os.path.realpath(__file__)
        currentDirectory = os.path.dirname(currentFile)
        load_dotenv(os.path.join(currentDirectory, ".env.datasource"))
        # Optional Firebase Initialization
        self.firebaseServiceAccountKeyPath = os.getenv("FIREBASE_SERVICE_ACCOUNT_KEY_PATH")
        self.setupFirebaseIfNeeded(self.firebaseServiceAccountKeyPath)

    def fetchStories(self) -> List[Story]:
        raise NotImplementedError("fetchStories() not implemented, make sure to override it in your plugin")

    def identify(self) -> str:
        raise NotImplementedError("identify() not implemented, make sure to override it in your plugin")

    def writePodcastDetails(self, podcastName, stories):
        raise NotImplementedError("writePodcastDetails() not implemented, make sure to override it in your plugin")

    def writeToDisk(self, story, storiesDirName, storyFileNameLambda):
        url = story["link"]
        uniqueId = story["uniqueId"]
        rawTextFileName = storyFileNameLambda(uniqueId, url)
        filePath = os.path.join(storiesDirName, rawTextFileName)
        os.makedirs(storiesDirName, exist_ok=True)
        with open(filePath, "w", encoding="utf-8") as file:
            json.dump(story, file)
            file.flush()

    def makeUniqueStoryIdentifier(self) -> str:
        characters = string.ascii_uppercase + string.ascii_lowercase + string.digits
        randomId = "".join(random.choice(characters) for _ in range(6))
        return randomId

    def doesOutputFileExist(self, story, storiesDirName, storyFileNameLambda) -> bool:
        url = story["link"]
        uniqueId = story["uniqueId"]
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

    def setupFirebaseIfNeeded(self, firebaseServiceAccountKeyPath):
        if firebaseServiceAccountKeyPath:
            if os.getenv("FIREBASE_DATABASE_URL") is None:
                raise ValueError("FIREBASE_DATABASE_URL environment variable is not set, please set it in .config.env and try again.")
            cred = credentials.Certificate(firebaseServiceAccountKeyPath)
            # check if firebase is already initialized
            if len(firebase_admin._apps) == 0:
                firebase_admin.initialize_app(
                    cred,
                    {"databaseURL": os.getenv("FIREBASE_DATABASE_URL")},
                )

    def parseDate(self, dateString):
        dateFormats = ["%a, %d %b %Y %H:%M:%S %Z", "%a, %d %b %Y %H:%M:%S %z"]
        for fmt in dateFormats:
            try:
                return datetime.strptime(dateString, fmt)
            except ValueError:
                pass
        raise ValueError(f"time data '{dateString}' does not match any format")
