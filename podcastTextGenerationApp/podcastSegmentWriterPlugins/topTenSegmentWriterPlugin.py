import yaml

from podcastSegmentWriterPlugins.baseSegmentWriterPlugin import BaseSegmentWriterPlugin
from podcastSegmentWriterPlugins.utilities.storySegmentWriter import StorySegmentWriter


class TopTenSegmentWriterPlugin(BaseSegmentWriterPlugin):
    def identify(self) -> str:
        return "TopTenSegmentWriterPlugin"

    def writeStorySegment(self, story):
        url = story["link"]
        print("Writing Segment: " + url)
        storyCopy = story.copy()
        for key in story["keysToIgnoreForWritingSegment"]:
            if key in storyCopy:
                del storyCopy[key]
        storySummary = self.cleanupStorySummary(
            yaml.dump(storyCopy, default_flow_style=False)
        )
        storyText = StorySegmentWriter().writeSegmentFromSummary(storySummary)
        return storyText


plugin = TopTenSegmentWriterPlugin()
