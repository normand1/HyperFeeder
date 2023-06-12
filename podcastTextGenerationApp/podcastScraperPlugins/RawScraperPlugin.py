from podcastScraperPlugins.abstractPluginDefinitions.abstractStoryScraperPlugin import AbstractStoryScraperPlugin
import requests
import os

class RawScraperPlugin(AbstractStoryScraperPlugin):

    def identify(self) -> str:
        return "RawScraperPlugin"

    def scrapeSitesForText(self, topStories, rawTextDirName, rawTextFileNameLambda):
        print("Scraping news sites for text...")
        for story in topStories:
            url = story["link"]
            rawTextFileName = rawTextFileNameLambda(story["newsRank"], url)
            filePath = os.path.join(rawTextDirName, rawTextFileName)
            if os.path.exists(filePath):
                    print("raw text file already exists for url: " + url + ", skipping scraping story")
                    break
            else:
                print("Scraping: " + url)
                raw_text_from_url_response = requests.get(url)
                if raw_text_from_url_response.text:
                    os.makedirs(rawTextDirName, exist_ok=True)
                with open(filePath, 'w') as file:
                    file.write(raw_text_from_url_response.text)
                    file.flush()

plugin = RawScraperPlugin()