import requests
import re

class ScrapEurosportFootball:
    def __init__(self):
        self.url = 'https://www.eurosport.com/football/'
        self.link_pattern = re.compile(r'https?://[^\s]+')
        self.links = []

    def scrape(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            self.extract_links(response.text)
            self.filter_links()
            self.save_links()
        else:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

    def extract_links(self, content):
        self.links = self.link_pattern.findall(content)

    def filter_links(self):
        self.links = [link for link in self.links if link.startswith(self.url) and link.endswith('story.shtml"')]
        self.links = [link.rstrip('"') for link in self.links]

    def save_links(self):
        with open('links.csv', 'w') as file:
            file.write('Links\n')
            for link in self.links:
                file.write(link + '\n')

# Usage
scraper = ScrapEurosportFootball()
scraper.scrape()
