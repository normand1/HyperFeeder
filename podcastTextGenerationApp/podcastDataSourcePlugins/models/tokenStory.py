from podcastDataSourcePlugins.models.story import Story
from podcastDataSourcePlugins.models.warpcastUser import WarpcastUser


class TokenStory(Story):
    @classmethod
    def from_dict(cls, story_dict):
        """Create a TokenStory instance from a dictionary"""
        if story_dict.get("storyType") != "Token":
            return None

        return cls(
            contract_address=story_dict.get("contract_address"),
            name=story_dict.get("name"),
            symbol=story_dict.get("symbol"),
            time_ago=story_dict.get("time_ago"),
            creator_name=story_dict.get("creator_name"),
            creator_link=story_dict.get("creator_link"),
            creator_username=story_dict.get("creator_username"),
            image_url=story_dict.get("image_url"),
            dexscreener_url=story_dict.get("dexscreener_url"),
            basescan_url=story_dict.get("basescan_url"),
            clanker_url=story_dict.get("clanker_url"),
            uniqueId=story_dict.get("uniqueId"),
        )

    def __init__(self, contract_address, name, symbol, time_ago, creator_name, creator_link, creator_username, image_url, dexscreener_url, basescan_url, clanker_url, uniqueId):
        super().__init__(0, name, clanker_url, "Token", uniqueId, "Clanker")
        self.contract_address = contract_address
        self.name = name
        self.symbol = symbol
        self.time_ago = time_ago
        self.creator_name = creator_name
        self.creator_link = creator_link
        self.creator_username = creator_username
        self.image_url = image_url
        self.dexscreener_url = dexscreener_url
        self.basescan_url = basescan_url
        self.clanker_url = clanker_url
        self.uniqueId = uniqueId
        self.warpcast_user = None  # Initialize as None
        self.keysToIgnoreForWritingSegment.append("creator_link")
        self.keysToIgnoreForWritingSegment.append("image_url")
        self.keysToIgnoreForWritingSegment.append("dexscreener_url")
        self.keysToIgnoreForWritingSegment.append("basescan_url")
        self.keysToIgnoreForWritingSegment.append("clanker_url")
        self.keysToIgnoreForWritingSegment.append("uniqueId")

    def set_warpcast_user(self, user_data):
        """Set the WarpcastUser for this token story"""
        self.warpcast_user = WarpcastUser(user_data) if user_data else None

    def __json__(self, depth=10):
        """Make the class directly JSON serializable"""
        return {
            "contract_address": str(self.contract_address),
            "name": str(self.name),
            "symbol": str(self.symbol),
            "time_ago": str(self.time_ago),
            "creator_name": str(self.creator_name),
            "creator_link": str(self.creator_link),
            "creator_username": str(self.creator_username),
            "image_url": str(self.image_url),
            "dexscreener_url": str(self.dexscreener_url),
            "basescan_url": str(self.basescan_url),
            "clanker_url": str(self.clanker_url),
            "uniqueId": str(self.uniqueId),
            "storyType": "Token",
            "link": str(self.clanker_url),
            "warpcast_user": self.warpcast_user.__json__() if self.warpcast_user else None,
        }
