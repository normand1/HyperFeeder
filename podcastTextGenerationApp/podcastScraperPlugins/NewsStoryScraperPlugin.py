import json
import os

from podcastScraperPlugins.abstractPluginDefinitions.abstractStoryScraperPlugin import AbstractStoryScraperPlugin
from newsScraper import NewsScraper
from langchain.text_splitter import CharacterTextSplitter

class NewsStoryScraperPlugin(AbstractStoryScraperPlugin):

    def identify(self) -> str:
        return "NewsStoryScraperPlugin"

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
                texts = self.scrapeAndPrepareStoryText(url)
                
                os.makedirs(rawTextDirName, exist_ok=True)
                
                with open(filePath, 'w') as file:
                    file.write(json.dumps(texts))
                    file.flush()

    def scrapeAndPrepareStoryText(self, url):
        scraper = NewsScraper()
        try:
            article = scraper.scrape(url)

            # Prepare text for summarization
            text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
                separator='.\n',
                chunk_size=1000,
                chunk_overlap=0 # no overlap
            )
            texts = text_splitter.split_text(article)
            return texts
        except:
            print("Scraping failed, skipping story")
            return "This story could not be scraped. Please replace this text with any text you can find at this url: \n" + url + " \n and re-run the script."

plugin = NewsStoryScraperPlugin()