from podcastDataSourcePlugins.models.story import Story
from podcastDataSourcePlugins.abstractPluginDefinitions.abstractDataSourcePlugin import AbstractDataSourcePlugin
from typing import List
import os
import json
import random
import string
from urllib.parse import urlparse

class BaseDataSourcePlugin(AbstractDataSourcePlugin):
    def fetchStories(self) -> List[Story]:
        raise Exception("fetchStories() not implemented")
    def identify(self) -> str:
        raise Exception("identify() not implemented")
    def writePodcastDetails(self, podcastName, topStories):
        raise Exception("writePodcastDetails() not implemented")
    def writeToDisk(self, story, storiesDirName, storyFileNameLambda):
        url = story["link"]
        uniqueId = story["uniqueId"]
        rawTextFileName = storyFileNameLambda(uniqueId, url)
        filePath = os.path.join(storiesDirName, rawTextFileName)
        os.makedirs(storiesDirName, exist_ok=True)
        with open(filePath, 'w') as file:
            json.dump(story, file)
            file.flush()
    def makeUniqueStoryIdentifier(self) -> str:
        characters = string.ascii_uppercase + string.ascii_lowercase + string.digits
        random_id = ''.join(random.choice(characters) for _ in range(6))
        return random_id
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
        filename = filename.replace('/', '_') # Replace slashes with underscores
        filename = filename.replace(':', '_') # Replace colons with underscores
        filename = filename.replace('-', '_') # Replace dashes with underscores
        return filename