import requests
import os
from bs4 import BeautifulSoup
from goose3 import Goose
from newsplease import NewsPlease
from dotenv import load_dotenv


class NewsScraper:

    def __init__(self):
        load_dotenv()

    def scrape(self, url):
        try:
            # Try scraping with Jina API
            jina_url = f"https://r.jina.ai/{url}"
            headers = {"Authorization": f"Bearer {os.getenv('JINA_API_KEY')}"}
            response = requests.get(jina_url, headers=headers)
            response.raise_for_status()
            text = response.text
            if not text:
                raise Exception("No text found with Jina API")
            return text
        except Exception as e5:
            print(f"Jina API failed: {e5}")
            raise Exception("No text could be scraped")


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
