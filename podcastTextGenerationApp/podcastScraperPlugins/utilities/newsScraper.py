import requests
from dotenv import load_dotenv
from podcastSegmentWriterPlugins.utilities.utils import storyCouldNotBeScrapedText


class NewsScraper:

    def __init__(self):
        load_dotenv()

    def scrape(self, url):
        try:
            # Try scraping with Jina API
            jina_url = f"https://r.jina.ai/{url}"
            # headers = {"Authorization": f"Bearer {os.getenv('JINA_API_KEY')}"}
            response = requests.get(jina_url)
            text = response.text
            if not text:
                return f"{storyCouldNotBeScrapedText()}\n{url}"
            return text
        except Exception as e5:
            print(f"Jina API failed: {e5}")
            return f"{storyCouldNotBeScrapedText()}\n{url}"


if __name__ == "__main__":
    # get url from user
    url = input("Enter a url: ")
    # scrape the url
    try:
        scraper = NewsScraper()
        article = scraper.scrape(url)
        # print the article
        print(article)
    except Exception as e:
        print(f"Scraping failed: {e}")
