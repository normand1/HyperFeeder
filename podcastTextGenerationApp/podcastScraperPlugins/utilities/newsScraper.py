import requests
from dotenv import load_dotenv
import time


class NewsScraper:

    def __init__(self):
        load_dotenv()

    def scrape(self, url):
        try:
            # Try scraping with Jina API
            jina_url = f"https://r.jina.ai/{url}"
            # headers = {"Authorization": f"Bearer {os.getenv('JINA_API_KEY')}"}
            response = requests.get(jina_url)
            print(response)
            time.sleep(10)
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
