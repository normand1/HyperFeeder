import yaml
import os

from podcastSegmentWriterPlugins.abstractPluginDefinitions.abstractSegmentWriterPlugin import AbstractSegmentWriterPlugin
from storySegmentWriter import StorySegmentWriter

class TopTenSegmentWriterPlugin(AbstractSegmentWriterPlugin):

    def identify(self) -> str:
        return "TopTenSegmentWriterPlugin"
    
    def writeStorySegment(self, topStories, segmentTextDirNameLambda, segmemntTextFileNameLambda):
        for story in topStories:
            url = story["link"]
            print("Writing Segment: " + url)
            filePath = os.path.join(segmentTextDirNameLambda, segmemntTextFileNameLambda(story["newsRank"], url))
            if not os.path.isfile(filePath):
                directory = os.path.dirname(filePath)
                os.makedirs(directory, exist_ok=True)  # Create the necessary directories
                with open(filePath, 'w') as file:
                    try:
                        del story["rawSplitText"]
                        del story["rawText"]
                    except:
                        pass
                    storyText = StorySegmentWriter().writeSegmentFromSummary(yaml.dump(story, default_flow_style=False))
                    try:
                        file.write(storyText + "\n")
                        file.flush()
                    except:
                        print("Error writing to file")
            else:
                print("story file already exists... nothing else to do for this story: " + filePath)
    

plugin = TopTenSegmentWriterPlugin()