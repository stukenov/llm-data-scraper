from parse_sitemaps import ParseSitemaps
import logging
from db import ScraperDatabase
from time import sleep
from scraper import Scraper

scraper_db = ScraperDatabase()
parse_sitemaps = ParseSitemaps()
scraper = Scraper()

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def parse_and_insert(source_name, parse_function):
    try:
        logging.info(f'Parsing {source_name}')
        parsed_links = parse_function()
        logging.debug(f'Parsed links: {parsed_links}')
        logging.info(f'Parsed {len(parsed_links)} links from {source_name}')
        sleep(5)
    except Exception as e:
        logging.error(e, exc_info=True)
        return

    try:
        logging.info(f'Checking link is parsed?')
        link_is_parsed = scraper_db.link_is_parsed(parsed_links)
        logging.debug(f'Link parsed check result for {parsed_links}: {link_is_parsed}')
        if link_is_parsed:
            logging.info(f'Link is parsed, skipping')
            return
        else:
            logging.info(f'Link is not parsed, scraping')
    except Exception as e:
        logging.error(e, exc_info=True)

    try:
        logging.info(f'Scraping {source_name} text content')
        scraped_content_result = scraper.get_text_content(parsed_links)
        logging.info(f'Scraped {source_name} text content')
        logging.debug(f'Scraped content result for {source_name}: {scraped_content_result}')
    except Exception as e:
        logging.error(e, exc_info=True)
        sleep(10)

    try:
        logging.info(f'Scraping {source_name} og image')
        og_image_url = scraper.get_og_image(parsed_links)
        logging.info(f'Scraped {source_name} og image')
        logging.debug(f'OG image URL for {source_name}: {og_image_url}')
    except Exception as e:
        logging.error(e, exc_info=True)
        sleep(10)

    try:
        logging.info(f'Inserting {source_name} to database')
        publish_to_db = scraper_db.insert_link_content(url=parsed_links, source=source_name, scraped_content=scraped_content_result, og_image_url=og_image_url)
        logging.info(f'Inserted {source_name} to database')
        logging.debug(f'Insert details - URL: {parsed_links}, Source: {source_name}, Scraped Content: {scraped_content_result}, OG Image URL: {og_image_url}')
        sleep(5)
    except Exception as e:
        logging.error(e, exc_info=True)
        sleep(10)

sources = [
    ('tengrinews', parse_sitemaps.parse_tengrinews),
    ('nur', parse_sitemaps.parse_nur),
    ('informburo', parse_sitemaps.parse_informburo),
    ('newtimes', parse_sitemaps.parse_newtimes),
    ('golosnaroda', parse_sitemaps.parse_golosnaroda),
    ('almatytv', parse_sitemaps.parse_almatytv),
    ('lada', parse_sitemaps.parse_lada),
    ('inbusiness', parse_sitemaps.parse_inbusiness),
    # ('alau', parse_sitemaps.parse_alau),
    # ('vesti_kz', parse_sitemaps.parse_vesti_kz),
    ('liter', parse_sitemaps.parse_liter),
    ('sputnik', parse_sitemaps.parse_sputnik)
]


while True:
    for source_name, parse_function in sources:
        parse_and_insert(source_name, parse_function)

