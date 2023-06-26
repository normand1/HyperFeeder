from abc import abstractmethod
import os, json
from podcastSummaryPlugins.abstractPluginDefinitions.abstractStorySummaryPlugin import AbstractStorySummaryPlugin

class BaseSummaryPlugin(AbstractStorySummaryPlugin):
    @abstractmethod
    def summarizeText(self, story):
        pass
    @abstractmethod
    def identify(self) -> str:
        pass
    def writeToDisk(self, story, summaryText, summaryTextDirName, summaryTextFileNameLambda):
        url = story["link"]
        uniqueId = story["uniqueId"]
        rawTextFileName = summaryTextFileNameLambda(uniqueId ,url)
        filePath = os.path.join(summaryTextDirName, rawTextFileName)
        os.makedirs(summaryTextDirName, exist_ok=True)
        with open(filePath, 'w') as file:
            json.dump(summaryText, file)
            file.flush()
    def doesOutputFileExist(self, story, summaryTextDirName, summaryTextFileNameLambda) -> bool:
        url = story["link"]
        uniqueId = story["uniqueId"]
        rawTextFileName = summaryTextFileNameLambda(uniqueId, url)
        filePath = os.path.join(summaryTextDirName, rawTextFileName)
        if os.path.exists(filePath):
            print("Summary text file already exists at filepath: " + filePath + ", skipping summarizing story")
            return True
        else:
            return False
    