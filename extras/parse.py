import requests
from bs4 import BeautifulSoup
from contextlib import closing

class NewsParser:
    def __init__(self, url):
        self.url = url

    def fetch_web_page(self):
        try:
            with requests.get(self.url) as response:
                response.raise_for_status()
                return response.content
        except requests.RequestException as e:
            print(f"HTTP Request failed: {e}")
            return None

    @staticmethod
    def extract_news_articles(web_page_content):
        soup = BeautifulSoup(web_page_content, 'html.parser')
        return soup.find_all('article')

    @staticmethod
    def clean_article(article):
        soup = BeautifulSoup(str(article), 'html.parser')
        return soup.get_text().strip()

    @staticmethod
    def save_articles_to_file(articles, file_path):
        with open(file_path, 'w') as file:
            for article in articles:
                file.write(article + "\n\n")

    def parse(self):
        web_page_content = self.fetch_web_page()
        if web_page_content:
            articles = self.extract_news_articles(web_page_content)
            cleaned_articles = [self.clean_article(article) for article in articles]
            return cleaned_articles
        return []

if __name__ == "__main__":
    url_to_parse = "http://example.com/news"
    output_file_path = "cleaned_news_articles.txt"

    parser = NewsParser(url_to_parse)
    cleaned_articles = parser.parse()
    parser.save_articles_to_file(cleaned_articles, output_file_path)
