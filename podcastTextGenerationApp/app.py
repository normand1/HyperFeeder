import os
import sys
import yaml
import json

from langchain.text_splitter import CharacterTextSplitter
from dotenv import load_dotenv
from newsScraper import NewsScraper
from storySummarizer import StorySummarizer
from storySegmentWriter import StorySegmentWriter
from hackerNewsAPI import HackerNewsAPI
from podcastIntroWriter import PodcastIntroWriter


class App:
    def __init__(self):
        load_dotenv()

    def run(self, podcastName):
        hackerNewsAPI = HackerNewsAPI()
        top_stories = hackerNewsAPI.fetch_top_stories()
        top_stories.insert(0, {"title": "Presented by the Hypercatcher Podcast App", "link": "https://hypercatcher.com/", "hackerNewsRank": 0})
        os.makedirs(podcastName, exist_ok=True)
        with open(podcastName + "/podcastDetails.json", 'w') as file:
            json.dump(top_stories, file)

        file_name_intro = podcastName + "/intro_text/" + "intro.txt" 
        storyTitles = list(map(lambda story: story["title"], top_stories[1:]))

        self.writeIntroSegment(storyTitles, file_name_intro) # Write the Intro to disk

        for story in top_stories[1:]:
            url = story["link"]
            print("Scraping: " + url)
            file_name_summary = podcastName + "/summary_text/" + str(story["hackerNewsRank"]) + "-" + url.split("/")[-2] + ".txt" 
            file_name_story = podcastName + "/text/" + str(story["hackerNewsRank"]) + "-" + url.split("/")[-2] + ".txt" 
            try:
                texts = self.scrapeAndPrepareStoryText(url)
            except:
                print("Scraping failed, skipping story")
                texts = "This story could not be scraped and summarized. Please replace this text with any text you can find at this url: \n" + url
                story['hasError'] = True
        
            print("Summarizing: " + url)
            story = self.writeAndUpdateStorySummary(texts, file_name_summary, story) # Write the Summary to disk
            print("Writing Segment for: " + url)
            self.writeStorySegment(texts, file_name_story, story) # Write the Segment to disk

    def writeIntroSegment(self, storyTitles, file_name_intro):
        if not os.path.isfile(file_name_intro):
            directory = os.path.dirname(file_name_intro)
            os.makedirs(directory, exist_ok=True)
            with open(file_name_intro, 'w') as file:
                introText = PodcastIntroWriter().writeIntro(storyTitles)
                file.write(introText)
        else:
            print("intro file already exists, skipping writing intro")

    def scrapeAndPrepareStoryText(self, url):
        scraper = NewsScraper()
        article = scraper.scrape(url)

        # Prepare text for summarization
        text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
            separator='.\n',
            chunk_size=1000,
            chunk_overlap=0 # no overlap
        )
        texts = text_splitter.split_text(article)
        return texts

    def writeAndUpdateStorySummary(self, texts, file_name_summary, story):
        if not os.path.isfile(file_name_summary):
            directory = os.path.dirname(file_name_summary)
            os.makedirs(directory, exist_ok=True)  # Create the necessary directories
            with open(file_name_summary, 'w') as file:
                if 'hasError' in story:
                    summaryText = "This story could not be scraped and summarized. Please replace this text with any text you can find at this url: \n" + story["link"]
                else:
                    summaryText = StorySummarizer().summarize(" ".join(texts[:2]))
                file.write(summaryText + "\n")
                file.flush()
                if 'hasError' in story:
                    raise Exception("Story has error")
                story["summary"] = summaryText
        else:
            print("summary file already exists")
            # read text from file
            with open(file_name_summary, 'r') as file:
                texts = file.readlines()
                # combine all the text into a single string
                texts = " ".join(texts)
                story["summary"] = texts
        return story

    def writeStorySegment(self, texts, file_name_story, story):
        if 'hasError' in story:
            print("Skipping writing story segment because story has error")
            return
        if not os.path.isfile(file_name_story):
            directory = os.path.dirname(file_name_story)
            os.makedirs(directory, exist_ok=True)  # Create the necessary directories
            with open(file_name_story, 'w') as file:
                storyText = StorySegmentWriter().writeSegmentFromSummary(yaml.dump(story, default_flow_style=False))
                try:
                    # file.write(storyText + "\n")
                    file.write(storyText + "\n")
                    file.flush()
                except:
                    print("Error writing to file")
        else:
            print("story file already exists... nothing else to do for this story: " + file_name_story)
                
if __name__ == "__main__":
    app = App()
    if len(sys.argv) > 1:
        parameter = sys.argv[1]  # Get the first parameter passed to the script
        app.run(parameter)
    else:
        podcastName = input("Enter a name for your podcast: ")
        app.run(podcastName)