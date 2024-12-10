import json
import os

from podcastResearcherPlugins.baseResearcherPlugin import BaseResearcherPlugin
from podcastDataSourcePlugins.models.tokenStory import TokenStory
from sharedPluginServices.neynarAPIManager import NeynarAPIManager


class WarpcastUserResearcherPlugin(BaseResearcherPlugin):
    # priority value needs to be lower than other research plugins that depend on the warpcast user
    priority = 99

    def __init__(self):
        super().__init__()
        self.neynarApiManager = NeynarAPIManager()

    def identify(self, simpleName=False) -> str:
        if simpleName:
            return "warpcastUser"
        else:
            return "👩🏻‍🎤 Warpcast User Researcher Plugin"

    def updateStories(self, segments: list[TokenStory]):

        for story in segments:
            # Fetch user info
            user = self.neynarApiManager.get_user_by_username(story.creator_username)
            print(user)
            story.set_warpcast_user(user)
        return segments

    def researchStories(self, segments: list[TokenStory], researchDirName: str):
        return None

    def writePodcastDetails(self, podcastName, segments):
        os.makedirs(podcastName, exist_ok=True)
        with open(podcastName + "/podcastDetails.json", "w", encoding="utf-8") as file:
            json.dump(segments, file)


plugin = WarpcastUserResearcherPlugin()
