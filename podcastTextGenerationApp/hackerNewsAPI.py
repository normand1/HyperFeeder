import requests

class HackerNewsAPI:
    def __init__(self):
        self.base_url = "https://hacker-news.firebaseio.com/v0/"

    def fetch_top_stories(self):
        top_stories_url = f"{self.base_url}topstories.json"
        response = requests.get(top_stories_url)
        top_stories_ids = response.json()

        stories = []

        for rank, story_id in enumerate(top_stories_ids[:5], 1):
            story_url = f"{self.base_url}item/{story_id}.json"
            response = requests.get(story_url)
            story_data = response.json()
            
            story = {
                "hackerNewsRank": rank,
                "title": story_data.get("title"),
                "link": story_data.get("url"),
                "storyType": story_data.get("type"),
                "source": "Hacker News"
            }
            stories.append(story)
        
        return stories