import yaml
from podcastSegmentWriterPlugins.baseSegmentWriterPlugin import BaseSegmentWriterPlugin
from podcastSegmentWriterPlugins.utilities.storySegmentWriter import StorySegmentWriter
from podcastDataSourcePlugins.models.segment import Segment
from utilities.xml_utils import strip_xml_tags
from utilities.textFilteringUtils import TextFilteringUtils


class GenericNewsPodcastSegmentWriter(BaseSegmentWriterPlugin):
    def identify(self) -> str:
        return "🎤 GenericNewsPodcastSegmentWriter"

    def writeStorySegment(self, story: Segment, segments):
        uuid = story.uniqueId
        print("Writing Segment: " + uuid)
        storyCopy = story.to_dict()
        if hasattr(story, "keysToIgnoreForWritingSegment"):
            for key in story.keysToIgnoreForWritingSegment:
                if key in storyCopy:
                    del storyCopy[key]
        storySummary = TextFilteringUtils.cleanupStorySummary(yaml.dump(storyCopy, default_flow_style=False))
        storyText = StorySegmentWriter().writeSegmentFromSummary(storySummary, story.title)
        storyText = TextFilteringUtils.cleanText(storyText)
        storyText = TextFilteringUtils.remove_links(storyText)
        storyText = TextFilteringUtils.cleanupStorySummary(storyText)
        storyText = strip_xml_tags(storyText)
        return storyText


plugin = GenericNewsPodcastSegmentWriter()
