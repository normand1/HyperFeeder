import json
import os

from podcastResearcherPlugins.baseResearcherPlugin import BaseResearcherPlugin
from podcastDataSourcePlugins.models.tokenStory import TokenStory


class TestResearcherPlugin(BaseResearcherPlugin):
    def __init__(self):
        super().__init__()

    def identify(self, simpleName=False) -> str:
        if simpleName:
            return "testResearcherPlugin"
        else:
            return "🧪📕 Test Researcher Plugin"

    def updateStories(self, segments: list[TokenStory]):
        return segments

    def researchStories(self, segments: list[TokenStory], researchDirName: str):
        searchResults = {}
        for story in segments:
            searchResults[story.uniqueId] = {"test": "test values"}
        return searchResults

    def writePodcastDetails(self, podcastName, segments):
        os.makedirs(podcastName, exist_ok=True)
        with open(podcastName + "/podcastDetails.json", "w", encoding="utf-8") as file:
            json.dump(segments, file)


plugin = TestResearcherPlugin()
