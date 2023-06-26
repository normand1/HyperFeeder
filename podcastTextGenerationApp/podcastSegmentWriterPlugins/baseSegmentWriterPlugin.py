from abc import abstractmethod
import os, json
from podcastSegmentWriterPlugins.abstractPluginDefinitions.abstractSegmentWriterPlugin import AbstractSegmentWriterPlugin

class BaseSegmentWriterPlugin(AbstractSegmentWriterPlugin):
    @abstractmethod
    def writeStorySegment(self, story, segmentTextDirNameLambda, segmemntTextFileNameLambda):
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
        with open(filePath, 'w') as file:
            json.dump(scrapedText, file)
            file.flush()
    def doesOutputFileExist(self, story, directory, fileNameLambda) -> bool:
        url = story["link"]
        uniqueId = story["uniqueId"]
        filename = fileNameLambda(uniqueId, url)
        filePath = os.path.join(directory, filename)
        if os.path.exists(filePath):
            print("Segment text file already exists at filepath: " + filePath + ", skipping writing segment for story")
            return True
        else:
            return False
    