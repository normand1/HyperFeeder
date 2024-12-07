import json
import os

from podcastResearcherPlugins.baseResearcherPlugin import BaseResearcherPlugin
from podcastDataSourcePlugins.models.tokenStory import TokenStory
from sharedPluginServices.neynarAPIManager import NeynarAPIManager


class WarpcastCastsResearcherPlugin(BaseResearcherPlugin):
    def __init__(self):
        super().__init__()
        self.neynarApiManager = NeynarAPIManager()

    def identify(self, simpleName=False) -> str:
        if simpleName:
            return "warpcastCasts"
        else:
            return "🎣 Warpcast Casts Researcher Plugin"

    def updateStories(self, stories: list[TokenStory]):
        return stories

    def researchStories(self, stories: list[TokenStory], researchDirName: str):
        searchResults = {}
        for story in stories:
            searchResults[story.uniqueId] = self.neynarApiManager.search_casts(story.title, author_fid=story.warpcast_user.fid)
        return searchResults

    def writePodcastDetails(self, podcastName, stories):
        os.makedirs(podcastName, exist_ok=True)
        with open(podcastName + "/podcastDetails.json", "w", encoding="utf-8") as file:
            json.dump(stories, file)


plugin = WarpcastCastsResearcherPlugin()
