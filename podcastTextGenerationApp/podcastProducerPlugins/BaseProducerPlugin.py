from abc import abstractmethod
import os
from podcastProducerPlugins.abstractPluginDefinitions.abstractProducerPlugin import (
    AbstractProducerPlugin,
)
from dotenv import load_dotenv


class BaseProducerPlugin(AbstractProducerPlugin):
    def __init__(self):
        currentFile = os.path.realpath(__file__)
        currentDirectory = os.path.dirname(currentFile)
        load_dotenv(os.path.join(currentDirectory, ".env.producer"))

    @abstractmethod
    def updateFileNames(
        self,
        stories,
        outroTextDirName,
        introDirName,
        segmentTextDirNameLambda,
        fileNameLambda,
    ):
        pass

    @abstractmethod
    def identify(self) -> str:
        pass

    def orderStories(self, stories):
        for index, story in enumerate(stories):
            story.itemOrder = index
            story.newsRank = index
        return stories

    def renameFile(self, directory, oldName, newName):
        # Construct the full old file name.
        oldFile = os.path.join(directory, oldName)

        # Construct the full new file name.
        newFile = os.path.join(directory, newName)
        try:
            os.rename(oldFile, newFile)
            print(f"File {oldName} has been successfully renamed to {newName}")
        except FileNotFoundError:
            print(f"The file {oldName} does not exist in the given directory")
        except OSError as error:
            print(f"An error occurred: {error}")
