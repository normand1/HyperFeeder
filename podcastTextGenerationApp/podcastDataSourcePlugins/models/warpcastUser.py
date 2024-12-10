class WarpcastUser:
    def __init__(self, user_data):
        user = user_data.get("user", {})
        self.fid = user.get("fid")
        self.username = user.get("username")
        self.display_name = user.get("display_name")
        self.pfp_url = user.get("pfp_url")
        self.custody_address = user.get("custody_address")
        self.bio = user.get("profile", {}).get("bio", {}).get("text")
        self.follower_count = user.get("follower_count")
        self.following_count = user.get("following_count")
        self.verifications = user.get("verifications", [])
        self.verified_eth_addresses = user.get("verified_addresses", {}).get("eth_addresses", [])
        self.verified_sol_addresses = user.get("verified_addresses", {}).get("sol_addresses", [])
        self.verified_accounts = user.get("verified_accounts")
        self.power_badge = user.get("power_badge", False)
        self.neynar_user_score = user.get("experimental", {}).get("neynar_user_score")

    def __json__(self, depth=10):
        return {
            "fid": self.fid,
            "username": self.username,
            "display_name": self.display_name,
            "pfp_url": self.pfp_url,
            "custody_address": self.custody_address,
            "bio": self.bio,
            "follower_count": self.follower_count,
            "following_count": self.following_count,
            "verifications": self.verifications,
            "verified_eth_addresses": self.verified_eth_addresses,
            "verified_sol_addresses": self.verified_sol_addresses,
            "verified_accounts": self.verified_accounts,
            "power_badge": self.power_badge,
            "neynar_user_score": self.neynar_user_score,
        }
