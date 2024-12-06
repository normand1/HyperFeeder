import requests
import whisper
from whisper.utils import get_writer
import os
import time
import re

from podcastScraperPlugins.baseStoryScraperPlugin import BaseStoryScraperPlugin


class PodcastRssAudioTranscriptScraper(BaseStoryScraperPlugin):

    def __init__(self):
        self.model = whisper.load_model("base")

    def identify(self) -> str:
        return "🎧🎙️ PodcastRssAudioTranscriptScraper"

    def doesHandleStory(self, story) -> bool:
        return getattr(story, "storyType", False) == "Podcast"

    def scrapeSiteForText(self, story, storiesDirName) -> str:
        enclosureLink = story.get("podcastEpisodeLink")
        if not enclosureLink:
            return None

        self.fetchAudioTranscriptFromRSS(enclosureLink, storiesDirName)

        # Create the same filename as in fetchAudioTranscriptFromRSS
        safe_filename = self.url_to_filename(enclosureLink)
        srt_filepath = os.path.join(storiesDirName, safe_filename + ".srt")

        # Read the contents of the SRT file
        if os.path.exists(srt_filepath):
            with open(srt_filepath, "r", encoding="utf-8") as srt_file:
                srt_content = srt_file.read()

            # Remove timecodes and line numbers from SRT content
            lines = srt_content.split("\n")
            transcript_lines = [line for line in lines if not line.strip().isdigit() and not "-->" in line]
            transcript_text = " ".join(transcript_lines).strip()

            return transcript_text
        else:
            return f"Transcript file not found: {srt_filepath}"

    def url_to_filename(self, url):
        # Remove scheme (http://, https://, etc.)
        url = re.sub(r"^https?:\/\/", "", url)
        # Replace non-alphanumeric characters with underscores
        filename = re.sub(r"[^a-zA-Z0-9]", "_", url)
        # Limit filename length to 255 characters (common filesystem limit)
        return filename[:255]

    def fetchAudioTranscriptFromRSS(self, enclosureLink, storiesDirName):
        # Create a URL-safe filename
        safe_filename = self.url_to_filename(enclosureLink)
        audio_filepath = os.path.join(storiesDirName, safe_filename + ".mp3")

        # Download the audio file
        self.download_audio(enclosureLink, audio_filepath)

        # Transcribe the audio file using Whisper
        print(f"Transcribing audio file {audio_filepath}...")
        start_time = time.time()
        result = self.model.transcribe(audio_filepath, verbose=True)
        end_time = time.time()
        print(f"Transcription completed in {end_time - start_time:.2f} seconds.")

        # Save the transcription to an SRT file
        srt_filepath = os.path.splitext(audio_filepath)[0] + ".srt"
        srt_writer = get_writer("srt", os.path.dirname(srt_filepath))
        srt_writer(result, os.path.basename(srt_filepath))
        print(f"Transcription saved to {srt_filepath}")

    def download_audio(self, url, filepath):
        print(f"Downloading audio from {url} to {filepath}...")
        response = requests.get(url, timeout=10)

        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        with open(filepath, "wb") as f:
            f.write(response.content)
        print("Audio downloaded")

    print("Processing completed.")

    def scrapeResearchAndOrganizeForSegmentWriter(self, story, storiesDirName) -> dict:
        return {}


plugin = PodcastRssAudioTranscriptScraper()
