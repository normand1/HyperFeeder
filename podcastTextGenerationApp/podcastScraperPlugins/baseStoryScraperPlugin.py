from podcastScraperPlugins.abstractPluginDefinitions.abstractStoryScraperPlugin import (
    AbstractStoryScraperPlugin,
)
from podcastDataSourcePlugins.models.story import Story
import os, json
from dotenv import load_dotenv
import re
from collections import OrderedDict
import glob


class BaseStoryScraperPlugin(AbstractStoryScraperPlugin):
    def __init__(self):
        currentFile = os.path.realpath(__file__)
        currentDirectory = os.path.dirname(currentFile)
        load_dotenv(os.path.join(currentDirectory, ".env.scraper"))

    def scrapeSiteForText(self, story, storiesDirName) -> str:
        pass

    def identify(self) -> str:
        pass

    def doesHandleStory(self, story) -> bool:
        pass

    def writeToDisk(self, story: Story, scrapedText, storiesDirName, storyFileNameLambda):
        url = story.link
        uniqueId = story.uniqueId
        rawTextFileName = storyFileNameLambda(uniqueId, url)
        filePath = os.path.join(storiesDirName, rawTextFileName)
        os.makedirs(storiesDirName, exist_ok=True)
        with open(filePath, "w", encoding="utf-8") as file:
            json.dump(scrapedText, file)
            file.flush()

    def doesOutputFileExist(self, story: Story, storiesDirName, storyFileNameLambda) -> bool:
        url = story.link
        uniqueId = story.uniqueId
        rawTextFileName = storyFileNameLambda(uniqueId, url)
        filePath = os.path.join(storiesDirName, rawTextFileName)
        if os.path.exists(filePath):
            print("Scraped text file already exists at filepath: " + filePath + ", skipping scraping story")
            return True
        else:
            return False

    def cleanupText(self, text):
        # Extract all links and their corresponding text
        link_pattern = re.compile(r"\[([^\]]+)\]\((https?://[^\)]+)\)")
        links = link_pattern.findall(text)

        # Use an OrderedDict to remove duplicates while preserving order
        unique_links = OrderedDict((link, url) for link, url in links)

        # Reconstruct the cleaned text
        cleaned_text = link_pattern.sub("", text)  # Remove all links from the text
        for link, url in unique_links.items():
            cleaned_text += f"[{link}]({url})\n"

        return cleaned_text

    def readResearchFromDisk(self, story: Story, researchDirName) -> dict[str, dict]:
        allResearch = {}
        storyDir = os.path.join(researchDirName, story.uniqueId)

        # Use glob to find all files in the directory
        filePaths = glob.glob(os.path.join(storyDir, "*"))

        for filePath in filePaths:
            with open(filePath, "r", encoding="utf-8") as file:
                # Extract researchType from the filename
                fileName = os.path.basename(filePath)
                researchType = fileName.split("-")[0]
                allResearch[researchType] = json.load(file)

        return allResearch

    def scrapeResearchAndOrganizeForSegmentWriter(self, story, storiesDirName, researchDirectoryName):
        pass
