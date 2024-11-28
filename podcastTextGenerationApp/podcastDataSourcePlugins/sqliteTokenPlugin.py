import json
import os
import sqlite3
from typing import List

from podcastDataSourcePlugins.baseDataSourcePlugin import BaseDataSourcePlugin
from podcastDataSourcePlugins.models.tokenStory import TokenStory


class SQLiteTokenPlugin(BaseDataSourcePlugin):
    def __init__(self):
        super().__init__()
        self.db_path = "/Users/davidnorman/clanker-launch-bot/tokens.db"

    def identify(self) -> str:
        return "💰 Token Database Plugin"

    def fetchStories(self) -> List[TokenStory]:
        stories = []

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Get the 5 most recent tokens
        cursor.execute(
            """
            SELECT contract_address, name, symbol, time_ago, creator_name, creator_link,
                   image_url, dexscreener_url, basescan_url, clanker_url
            FROM tokens
            ORDER BY created_at DESC
            LIMIT 5
        """
        )

        rows = cursor.fetchall()

        for row in rows:
            story = TokenStory(
                contract_address=row[0],
                name=row[1],
                symbol=row[2],
                time_ago=row[3],
                creator_name=row[4],
                creator_link=row[5],
                image_url=row[6],
                dexscreener_url=row[7],
                basescan_url=row[8],
                clanker_url=row[9],
                uniqueId=row[0],
            )
            stories.append(story.to_dict())

        conn.close()
        return stories

    def writePodcastDetails(self, podcastName, stories):
        os.makedirs(podcastName, exist_ok=True)
        with open(podcastName + "/podcastDetails.json", "w", encoding="utf-8") as file:
            json.dump(stories, file)


plugin = SQLiteTokenPlugin()
