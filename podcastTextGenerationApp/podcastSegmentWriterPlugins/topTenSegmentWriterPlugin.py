import yaml

from podcastSegmentWriterPlugins.baseSegmentWriterPlugin import BaseSegmentWriterPlugin
from podcastSegmentWriterPlugins.utilities.storySegmentWriter import StorySegmentWriter


class TopTenSegmentWriterPlugin(BaseSegmentWriterPlugin):
    def identify(self) -> str:
        return "🤙 TopTenSegmentWriterPlugin"

    def writeStorySegment(self, story, stories):
        url = story["link"]
        print("Writing Segment: " + url)
        storyCopy = story.copy()
        if "keysToIgnoreForWritingSegment" in story:
            for key in story["keysToIgnoreForWritingSegment"]:
                if key in storyCopy:
                    del storyCopy[key]
        storySummary = self.cleanupStorySummary(
            yaml.dump(storyCopy, default_flow_style=False)
        )
        storyText = StorySegmentWriter("claude").writeSegmentFromSummary(
            storySummary, story["title"]
        )
        return storyText


plugin = TopTenSegmentWriterPlugin()
