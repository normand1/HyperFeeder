from podcastSegmentWriterPlugins.baseSegmentWriterPlugin import BaseSegmentWriterPlugin


class TesterSegmentWriter(BaseSegmentWriterPlugin):
    def identify(self) -> str:
        return "🧪📝 tester segment writer"

    def writeStorySegment(self, story, segments):
        assert story is not None
        assert hasattr(story, "uniqueId"), "Story must have uniqueId"
        assert hasattr(story, "to_dict"), "Story must have to_dict method"

        uuid = story.uniqueId
        print("Writing Segment: " + uuid)

        storyCopy = story.to_dict()
        assert storyCopy is not None
        return "test segment text"


plugin = TesterSegmentWriter()
