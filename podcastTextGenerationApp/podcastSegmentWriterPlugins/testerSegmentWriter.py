import yaml
import os

from podcastSegmentWriterPlugins.baseSegmentWriterPlugin import BaseSegmentWriterPlugin
from podcastSegmentWriterPlugins.utilities.storySegmentWriter import StorySegmentWriter

class TesterSegmentWriter(BaseSegmentWriterPlugin):

    def identify(self) -> str:
        return "tester segment writer"
    
    def writeStorySegment(self, story):
        assert story is not None
        assert story["link"] is not None
        return 'test segment text'

plugin = TesterSegmentWriter()