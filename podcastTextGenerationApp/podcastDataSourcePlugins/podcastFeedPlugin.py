from podcastDataSourcePlugins.abstractPluginDefinitions.abstractDataSourcePlugin import AbstractDataSourcePlugin
import requests
from xml.etree import ElementTree as ET
from podcastDataSourcePlugins.models.podcastStory import PodcastStory
import os

class PodcastTranscriptAPIPlugin(AbstractDataSourcePlugin):
    def __init__(self):
        self.feeds = []
    
    def identify(self) -> str:
        return "🎙️ Podcast Transcript API Plugin"
    
    def fetchStories(self):

        podcast_feeds = os.getenv("PODCAST_FEEDS")
        if not podcast_feeds:
            raise ValueError("PODCAST_FEEDS environment variable is not set")

        self.feeds = podcast_feeds.split(',')

        if not self.feeds:
            raise ValueError("No podcast feeds in .env file, please add one and try again.")
        stories = [] 
        for index, feed_url in enumerate(self.feeds):
            response = requests.get(feed_url)
            root = ET.fromstring(response.content)
            namespace = {'podcast': 'https://github.com/Podcastindex-org/podcast-namespace/blob/main/docs/1.0.md'}

            podcast_title = root.find('.//channel/title')
            firstItem = list(root.iterfind('.//channel/item', namespace))[0]
            episodeLink = firstItem.find('link')
            transcript = firstItem.find('podcast:transcript', namespace)
            podcastOrder = index + 1
            episodeTitle = firstItem.find('title')
            if transcript is not None:
                stories.append(PodcastStory(
                    podcastOrder=podcastOrder,
                    title=episodeTitle.text,
                    link=transcript.get('url'),
                    storyType="Podcast",
                    source=podcast_title.text,
                    podcastEpisodeLink=episodeLink.text
                ).to_dict())
        return stories
    
plugin = PodcastTranscriptAPIPlugin()