import yaml
import os
from podcastSegmentWriterPlugins.baseSegmentWriterPlugin import BaseSegmentWriterPlugin
from podcastSegmentWriterPlugins.utilities.storySegmentWriter import StorySegmentWriter
from podcastDataSourcePlugins.baseDataSourcePlugin import Story


class TopTenSegmentWriterPlugin(BaseSegmentWriterPlugin):
    def identify(self) -> str:
        return "🤙 TopTenSegmentWriterPlugin"

    def writeStorySegment(self, story: Story, stories):
        url = story.link
        print("Writing Segment: " + url)
        storyCopy = story.to_dict()
        if hasattr(story, "keysToIgnoreForWritingSegment"):
            for key in story.keysToIgnoreForWritingSegment:
                if key in storyCopy:
                    del storyCopy[key]
        storySummary = self.cleanupStorySummary(yaml.dump(storyCopy, default_flow_style=False))
        model_provider = os.environ["LLM_MODEL_PROVIDER"]
        storyText = StorySegmentWriter(model_provider).writeSegmentFromSummary(storySummary, story.title)
        return storyText


plugin = TopTenSegmentWriterPlugin()
