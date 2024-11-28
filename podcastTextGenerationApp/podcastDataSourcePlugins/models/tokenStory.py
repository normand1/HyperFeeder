from podcastDataSourcePlugins.models.story import Story


class TokenStory(Story):
    def __init__(self, contract_address, name, symbol, time_ago, creator_name, creator_link, image_url, dexscreener_url, basescan_url, clanker_url, uniqueId):
        super().__init__(0, name, clanker_url, "Token", uniqueId, "Clanker")
        self.contract_address = contract_address
        self.name = name
        self.symbol = symbol
        self.time_ago = time_ago
        self.creator_name = creator_name
        self.creator_link = creator_link
        self.image_url = image_url
        self.dexscreener_url = dexscreener_url
        self.basescan_url = basescan_url
        self.clanker_url = clanker_url
        self.uniqueId = uniqueId
        self.keysToIgnoreForWritingSegment.append("creator_link")
        self.keysToIgnoreForWritingSegment.append("image_url")
        self.keysToIgnoreForWritingSegment.append("dexscreener_url")
        self.keysToIgnoreForWritingSegment.append("basescan_url")
        self.keysToIgnoreForWritingSegment.append("clanker_url")
        self.keysToIgnoreForWritingSegment.append("uniqueId")

    def to_dict(self):
        return {
            "contract_address": self.contract_address,
            "name": self.name,
            "symbol": self.symbol,
            "time_ago": self.time_ago,
            "creator_name": self.creator_name,
            "creator_link": self.creator_link,
            "image_url": self.image_url,
            "dexscreener_url": self.dexscreener_url,
            "basescan_url": self.basescan_url,
            "clanker_url": self.clanker_url,
            "uniqueId": self.uniqueId,
            "storyType": "Token",
            "link": self.clanker_url,  # Using clanker_url as the main link
        }
