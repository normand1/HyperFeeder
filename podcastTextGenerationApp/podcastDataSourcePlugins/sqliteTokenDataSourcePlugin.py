import os
import sqlite3
from typing import List

from podcastDataSourcePlugins.baseDataSourcePlugin import BaseDataSourcePlugin
from podcastDataSourcePlugins.models.tokenStory import TokenStory
from json_utils import dump_json
from langchain_core.tools import tool
from colorama import Fore, Style


# This plugin is used to fetch token segments from a sqlite database
# It is currently made to be integrated with the clanker-fomo-bot and the tokens.db
# NOTE: You will need to have this project running locally in order use this plugin (for now, api coming soon hopefully)
# https://github.com/normand1/clanker-fomo-bot
class SQLiteTokenDataSourcePlugin(BaseDataSourcePlugin):

    @classmethod
    def identify(cls, simpleName=False) -> str:
        if simpleName:
            return "tokenDatabase"
        else:
            return "💰 Token Database Plugin"

    @staticmethod
    @tool(name_or_callable="SQLiteTokenDataSourcePlugin-_-getRecentTokens")
    def getRecentTokens(searchQuery: str = None) -> List[TokenStory]:
        """
        Get the most recent clanker meme tokens from the database
        """
        segments: List[TokenStory] = []
        dbPath = os.getenv("TOKEN_STORIES_DB_PATH")
        storiesLimit = os.getenv("TOKEN_STORIES_COUNT_LIMIT", "5")

        conn = sqlite3.connect(dbPath)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Get tokens from the last hour
        cursor.execute(
            """
            SELECT t.contract_address, t.name, t.symbol, t.time_ago, t.creator_name, t.creator_link,
                   t.image_url, t.dexscreener_url, t.basescan_url, t.clanker_url
            FROM tokens t
            JOIN creator_details cd ON t.contract_address = cd.contract_address
            WHERE t.created_at >= datetime('now', '-1 hour')
                AND cd.neynar_score > 0.95
            ORDER BY t.created_at DESC
            LIMIT ?
        """,
            (storiesLimit),
        )

        rows = cursor.fetchall()

        for row in rows:
            story = TokenStory(
                contract_address=row["contract_address"],
                name=row["name"],
                symbol=row["symbol"],
                time_ago=row["time_ago"],
                creator_name=row["creator_name"],
                creator_link=row["creator_link"],
                creator_username=row["creator_link"].split("https://warpcast.com/")[1],
                image_url=row["image_url"],
                dexscreener_url=row["dexscreener_url"],
                basescan_url=row["basescan_url"],
                clanker_url=row["clanker_url"],
                uniqueId=row["contract_address"],
            )
            segments.append(story)

        conn.close()
        print(f"{Fore.GREEN}{Style.BRIGHT}Fetched {len(segments)} segments from Token Database{Style.RESET_ALL}")
        return segments

    def writePodcastDetails(self, podcastName, segments):
        os.makedirs(podcastName, exist_ok=True)
        with open(podcastName + "/podcastDetails.json", "w", encoding="utf-8") as file:
            dump_json(segments, file)


plugin = SQLiteTokenDataSourcePlugin()
