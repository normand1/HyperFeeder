from podcastDataSourcePlugins.baseDataSourcePlugin import BaseDataSourcePlugin
from json_utils import dump_json
import os

from podcastDataSourcePlugins.models.story import Story


class TesterDataSourcePlugin(BaseDataSourcePlugin):
    def __init__(self):
        super().__init__()

    def identify(self) -> str:
        return "🧪 Tester Data Source Plugin"

    def fetchStories(self):
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
        with open(podcastName + "/podcastDetails.json", "w") as file:
            dump_json(stories, file)


plugin = TesterDataSourcePlugin()
