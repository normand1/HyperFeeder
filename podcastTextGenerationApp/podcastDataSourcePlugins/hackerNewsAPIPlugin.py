from podcastDataSourcePlugins.baseDataSourcePlugin import BaseDataSourcePlugin
import requests
import json
import os

from podcastDataSourcePlugins.models.hackerNewsStory import HackerNewsStory

class HackerNewsAPIPlugin(BaseDataSourcePlugin):
    def __init__(self):
        super().__init__()
        self.base_url = "https://hacker-news.firebaseio.com/v0/"
    
    def identify(self) -> str:
        return "👨‍🎤 Hacker News API Plugin"
    

    def fetchStories(self):
        top_stories_url = f"{self.base_url}topstories.json"
        response = requests.get(top_stories_url)
        top_stories_ids = response.json()

        stories = []

        for rank, story_id in enumerate(top_stories_ids[:5]):
            story_url = f"{self.base_url}item/{story_id}.json"
            response = requests.get(story_url)
            story_data = response.json()

            story = HackerNewsStory(
                newsRank=rank,
                title=story_data.get("title"),
                link=story_data.get("url"),
                storyType=story_data.get("type"),
                uniqueId=self.makeUniqueStoryIdentifier()
            )
            stories.append(story.to_dict())

        return stories
    
    def writePodcastDetails(self, podcastName, topStories):
        os.makedirs(podcastName, exist_ok=True)
        with open(podcastName + "/podcastDetails.json", 'w') as file:
            json.dump(topStories, file)

plugin = HackerNewsAPIPlugin()