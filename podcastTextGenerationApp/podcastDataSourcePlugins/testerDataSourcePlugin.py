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
        return mock stories for a test
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

    def writePodcastDetails(self, podcastName, stories):
        os.makedirs(podcastName, exist_ok=True)
        with open(podcastName + "/podcastDetails.json", "w", encoding="utf-8") as file:
            dump_json(stories, file)

    def filterForImportantContextOnly(self, subStoryContent: dict):
        keysToKeep = ["title"]
        return {key: subStoryContent[key] for key in keysToKeep if key in subStoryContent}


plugin = TesterDataSourcePlugin()
