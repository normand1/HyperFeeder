from abc import abstractmethod
from podcastScraperPlugins.abstractPluginDefinitions.abstractStoryScraperPlugin import AbstractStoryScraperPlugin
import os, json

class BaseStoryScraperPlugin(AbstractStoryScraperPlugin):
    @abstractmethod
    def scrapeSiteForText(self, story) -> str:
        pass
    @abstractmethod
    def identify(self) -> str:
        pass
    def writeToDisk(self, story, scrapedText, storiesDirName, storyFileNameLambda):
        url = story["link"]
        uniqueId = story["uniqueId"]
        rawTextFileName = storyFileNameLambda(uniqueId, url)
        filePath = os.path.join(storiesDirName, rawTextFileName)
        os.makedirs(storiesDirName, exist_ok=True)
        with open(filePath, 'w') as file:
            json.dump(scrapedText, file)
            file.flush()
    def doesOutputFileExist(self, story, storiesDirName, storyFileNameLambda) -> bool:
        url = story["link"]
        uniqueId = story["uniqueId"]
        rawTextFileName = storyFileNameLambda(uniqueId, url)
        filePath = os.path.join(storiesDirName, rawTextFileName)
        if os.path.exists(filePath):
            print("Scraped text file already exists at filepath: " + filePath + ", skipping scraping story")
            return True
        else:
            return False
    