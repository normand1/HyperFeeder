from podcastDataSourcePlugins.baseDataSourcePlugin import BaseDataSourcePlugin
from json_utils import dump_json
import os
from langchain_core.tools import tool
from podcastDataSourcePlugins.models.story import Story


class TesterDataSourcePlugin(BaseDataSourcePlugin):

    @classmethod
    def identify(cls, simpleName=False) -> str:
        if simpleName:
            return "tester"
        else:
            return "🧪 Tester Data Source Plugin"

    @staticmethod
    @tool(
        name_or_callable="TesterDataSourcePlugin-_-fetchStories",
    )
    def fetchStories(searchQuery: str = None):
        """
        return mock segments for a test
        """
        story1 = Story(
            1,
            "Test Story 1",
            "https://www.google.com?=1",
            "Test Story Type",
            "123",
            "Test Source",
        )
        story2 = Story(
            2,
            "Test Story 2",
            "https://www.google.com?=2",
            "Test Story Type",
            "124",
            "Test Source",
        )
        story3 = Story(
            3,
            "Test Story 3",
            "https://www.google.com?=3",
            "Test Story Type",
            "125",
            "Test Source",
        )

        return [story1, story2, story3]

    def writePodcastDetails(self, podcastName, segments):
        os.makedirs(podcastName, exist_ok=True)
        with open(podcastName + "/podcastDetails.json", "w", encoding="utf-8") as file:
            dump_json(segments, file)

    def filterForImportantContextOnly(self, subStoryContent: dict):
        keysToKeep = ["title"]
        return {key: subStoryContent[key] for key in keysToKeep if key in subStoryContent}

    def fetchContentForStory(self, story: Story):
        if not isinstance(story, Story):
            raise TypeError("Input must be a Story object")
        if not story or not hasattr(story, "link"):
            raise ValueError("Invalid Story object provided")
        if story.link is None:
            raise ValueError("Story link cannot be None")
        if not isinstance(story.link, str):
            raise TypeError("Story link must be a string")
        if not story.link.strip():
            raise ValueError("Story link cannot be empty")

        return "This is a test content"


plugin = TesterDataSourcePlugin()
