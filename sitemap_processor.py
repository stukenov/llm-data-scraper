import requests
import logging
from xml.etree import ElementTree

class SitemapProcessor:
    SITEMAP_NAMESPACE = "{http://www.sitemaps.org/schemas/sitemap/0.9}"

    @staticmethod
    def fetch_and_parse_xml(url):
        try:
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; +http://www.google.com/bot.html) Chrome/W.X.Y.Z Safari/537.36"})
            response.raise_for_status()
            return ElementTree.fromstring(response.content)
        except requests.RequestException as e:
            logging.error(f"Error fetching the sitemap: {e}")
        except ElementTree.ParseError as e:
            logging.error(f"Failed to parse the XML: {e}")
        return None

    @classmethod
    def get_sitemaps(cls, url, condition=None, sort_type='ASC'):
        sitemap_urls = []
        sitemap_index = cls.fetch_and_parse_xml(url)
        if sitemap_index:
            for sitemap in sitemap_index.findall(f"{cls.SITEMAP_NAMESPACE}sitemap"):
                loc = sitemap.find(f"{cls.SITEMAP_NAMESPACE}loc")
                if loc is not None and (condition is None or condition(loc.text)):
                    if sort_type == 'DESC':
                        sitemap_urls.insert(0, loc.text)
                    else:
                        sitemap_urls.append(loc.text)
        return sitemap_urls

    @classmethod
    def get_new_urls_from_sitemap(cls, url, fix_url_func=None, sort_type='ASC'):
        urls = []
        sitemap_index = cls.fetch_and_parse_xml(url)
        if sitemap_index:
            for url_elem in sitemap_index.findall(f".//{cls.SITEMAP_NAMESPACE}url"):
                loc = url_elem.find(f"{cls.SITEMAP_NAMESPACE}loc")
                if loc is not None:
                    url = loc.text
                    if fix_url_func:
                        url = fix_url_func(url)
                    if sort_type == 'DESC':
                        urls.insert(0, url)
                    else:
                        urls.append(url)
        return urls

