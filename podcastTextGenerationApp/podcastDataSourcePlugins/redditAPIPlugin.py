from podcastDataSourcePlugins.abstractPluginDefinitions.abstractDataSourcePlugin import AbstractDataSourcePlugin
import requests

from podcastDataSourcePlugins.models.redditStory import RedditStory

class RedditAPIPlugin(AbstractDataSourcePlugin):
    def __init__(self):
        self.base_url = "https://www.reddit.com/r/technology.json"
    
    def identify(self) -> str:
        return "🗞️ Reddit API Plugin"
    

    def fetchStories(self):
        response = requests.get(self.base_url, headers = {'User-agent': 'Mozilla/5.0'})
        data = response.json()
        
        stories = []

        for rank, post in enumerate(data["data"]["children"][:5], 1):
            story = RedditStory(
                newsRank=rank,
                title=post["data"].get("title"),
                link=post["data"].get("url"),
                storyType=post["data"].get("post_hint", "text"), # Default to 'text' if no post_hint.
                source="Reddit"
            )
            stories.append(story.to_dict())

        return stories
    

plugin = RedditAPIPlugin()