import yaml
import os

from podcastSegmentWriterPlugins.baseSegmentWriterPlugin import BaseSegmentWriterPlugin
from podcastSegmentWriterPlugins.utilities.storySegmentWriter import StorySegmentWriter

class TopTenSegmentWriterPlugin(BaseSegmentWriterPlugin):

    def identify(self) -> str:
        return "TopTenSegmentWriterPlugin"
    
    def writeStorySegment(self, story, segmentTextDirNameLambda, segmemntTextFileNameLambda):
        url = story["link"]
        print("Writing Segment: " + url)
        storyText = StorySegmentWriter().writeSegmentFromSummary(yaml.dump(story, default_flow_style=False))
        return storyText
    

plugin = TopTenSegmentWriterPlugin()