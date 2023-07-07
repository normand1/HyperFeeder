import requests
from bs4 import BeautifulSoup
from goose3 import Goose
from newsplease import NewsPlease


class NewsScraper:
    def scrape(self, url):
        try:
            article = NewsPlease.from_url(url)
            if article.maintext == None:
                raise Exception("No main text found")
            return article.maintext
        except:
            try:
                g = Goose()
                article = g.extract(url=url)
                if not article.cleaned_text:
                    raise Exception("No text found with Goose")
                return article._meta_description + article.cleaned_text
            except:
                try:
                    page = requests.get(url)
                    soup = BeautifulSoup(page.text, "html.parser")
                    text = " ".join([p.text for p in soup.find_all("p")])
                    if not text:
                        raise Exception("No text found with BeautifulSoup")
                    return text
                except:
                    try:
                        # Another BeautifulSoup approach, getting the text inside 'div' tags
                        page = requests.get(url)
                        soup = BeautifulSoup(page.text, "html.parser")
                        text = " ".join([div.text for div in soup.find_all("div")])
                        if not text:
                            raise Exception(
                                "No text found with BeautifulSoup (div method)"
                            )
                        return text
                    except Exception as e:
                        print(f"Scraping failed: {e}")
                        raise Exception("No text could be scraped")


if __name__ == "__main__":
    # get url from user
    url = input("Enter a url: ")
    # scrape the url
    try:
        scraper = NewsScraper()
        article = scraper.scrape(url)
        # print the article
        print(article.maintext)
    except:
        g = Goose()
        article = g.extract(url=url)
        print(article.cleaned_text)
