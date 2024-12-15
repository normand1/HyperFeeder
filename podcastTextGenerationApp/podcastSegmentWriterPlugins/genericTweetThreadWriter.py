import yaml
import os
from podcastSegmentWriterPlugins.baseSegmentWriterPlugin import BaseSegmentWriterPlugin
from podcastSegmentWriterPlugins.utilities.tweetThreadWriter import TweetThreadWriter
from podcastDataSourcePlugins.models.segment import Segment
from utilities.xml_utils import strip_xml_tags
from utilities.textFilteringUtils import TextFilteringUtils


class GenericTweetThreadWriter(BaseSegmentWriterPlugin):
    def identify(self) -> str:
        return "🦅 GenericTweetThreadWriter"

    def writeStorySegment(self, story: Segment, segments):
        uuid = story.uniqueId
        print("Writing Segment: " + uuid)
        storyCopy = story.to_dict()
        if hasattr(story, "keysToIgnoreForWritingSegment"):
            for key in story.keysToIgnoreForWritingSegment:
                if key in storyCopy:
                    del storyCopy[key]
        storySummary = TextFilteringUtils.cleanupStorySummary(yaml.dump(storyCopy, default_flow_style=False))
        tweetThread = TweetThreadWriter().writeTweetThreadFromSummary(storySummary, story.title)
        tweetThread = tweetThread["tweets"]
        return "\n".join(tweetThread)

    def writeToDisk(self, story: Segment, scrapedText, directory, fileNameLambda):
        uuid = story.uniqueId
        filename = fileNameLambda(uuid)
        filePath = os.path.join(directory, "tweet_thread", filename)
        os.makedirs(os.path.dirname(filePath), exist_ok=True)
        with open(filePath, "w", encoding="utf-8") as file:
            file.write(scrapedText)
            file.flush()


plugin = GenericTweetThreadWriter()
