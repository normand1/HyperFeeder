from abc import abstractmethod
import os
from podcastProducerPlugins.abstractPluginDefinitions.abstractProducerPlugin import AbstractProducerPlugin

class BaseProducerPlugin(AbstractProducerPlugin):
    @abstractmethod
    def updateFileNames(self, stories, outroTextDirName, introDirName, segmentTextDirNameLambda, fileName):
        pass
    @abstractmethod
    def identify(self) -> str:
        pass
    def rename_file(self, directory, old_name, new_name):
        # Construct the full old file name.
        old_file = os.path.join(directory, old_name)
        
        # Construct the full new file name.
        new_file = os.path.join(directory, new_name)
        try:
            os.rename(old_file, new_file)
            print(f'File {old_name} has been successfully renamed to {new_name}')
        except FileNotFoundError:
            print(f'The file {old_name} does not exist in the given directory')
        except Exception as e:
            print(f'An error occurred: {e}')