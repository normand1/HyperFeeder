import yaml
from podcastSegmentWriterPlugins.baseSegmentWriterPlugin import BaseSegmentWriterPlugin
from podcastSegmentWriterPlugins.utilities.storySegmentWriter import StorySegmentWriter
from podcastDataSourcePlugins.models.segment import Segment
from utilities.xml_utils import strip_xml_tags


class TopTenSegmentWriterPlugin(BaseSegmentWriterPlugin):
    def identify(self) -> str:
        return "🤙 TopTenSegmentWriterPlugin"

    def writeStorySegment(self, story: Segment, segments):
        uuid = story.uniqueId
        print("Writing Segment: " + uuid)
        storyCopy = story.to_dict()
        if hasattr(story, "keysToIgnoreForWritingSegment"):
            for key in story.keysToIgnoreForWritingSegment:
                if key in storyCopy:
                    del storyCopy[key]
        storySummary = self.cleanupStorySummary(yaml.dump(storyCopy, default_flow_style=False))
        storyText = StorySegmentWriter().writeSegmentFromSummary(storySummary, story.title)
        storyText = strip_xml_tags(storyText)
        return storyText


plugin = TopTenSegmentWriterPlugin()
