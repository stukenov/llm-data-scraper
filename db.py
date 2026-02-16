import dataset
from datetime import datetime


class ScraperDatabase:
    def __init__(self, db_url='sqlite:///scraper.db', lazy_db_url='sqlite:///lazy_scraper.db'):
        self.db_url = db_url
        self.lazy_db_url = lazy_db_url

    def insert_link(self, url, source, scraped_content=None, og_image_url=None, is_parsed=False):
        db = dataset.connect(self.db_url)
        table = db['links']
        table.insert_ignore(
            {
                'url': url, 
                'source': source, 
                'scraped_content': scraped_content, 
                'og_image_url': og_image_url, 
                'is_parsed': is_parsed, 
                'created_at': datetime.now(), 
                'action_type': 'rewrite'
            }, 
            ['url']
        )
        db.close()

    def insert_link_content(self, url, source, scraped_content=None, og_image_url=None, is_parsed=False):
        db = dataset.connect(self.db_url)
        table = db['links']
        table.insert_ignore(
            {
                'url': url, 
                'source': source, 
                'scraped_content': scraped_content, 
                'og_image_url': og_image_url, 
                'is_parsed': is_parsed, 
                'created_at': datetime.now(), 
                'action_type': 'rewrite'
            }, 
            ['url']
        )
        db.close()

    def insert_link_to_lazy_content(
                        self, url, source, scraped_content=None, og_image_url=None, is_parsed=False):
        db = dataset.connect(self.lazy_db_url)
        table = db['generated_content']
        table.insert(
            {
                'url': url, 
                'source': source, 
                'scraped_content': scraped_content, 
                'og_image_url': og_image_url, 
                'is_parsed': is_parsed, 
                'created_at': datetime.now(), 
                'action_type': 'rewrite'
            }
        )
        db.close()

    def link_is_parsed(self, url) -> bool:
        db = dataset.connect(self.db_url)
        table = db['links']
        result = table.find_one(url=url)
        db.close()
        return result is not None

    def insert_link_in_lazy_db(self, url, source, scraped_content=None, og_image_url=None, is_parsed=False):
        db = dataset.connect(self.lazy_db_url)
        table = db['links']
        table.insert_ignore(
            {
                'url': url, 
                'source': source, 
                'scraped_content': scraped_content, 
                'og_image_url': og_image_url, 
                'is_parsed': is_parsed, 
                'created_at': datetime.now(), 
                'action_type': 'rewrite'
            }, 
            ['url']
        )
        db.close()

    def link_is_parsed_in_lazy_db(self, url) -> bool:
        db = dataset.connect(self.lazy_db_url)
        table = db['links']
        result = table.find_one(url=url)
        db.close()
        return result is not None

    def mark_content_as_parsed(self, url):
        db = dataset.connect(self.db_url)
        table = db['links']
        find_by_url = table.find_one(url=url)
        get_finded_id = find_by_url['id']
        table.update({'id': get_finded_id, 'is_parsed': True}, ['id'])
        db.close()

    def mark_lazy_link_as_parsed(self, id):
        db = dataset.connect(self.lazy_db_url)
        table = db['links']
        table.update({'id': id, 'is_parsed': True}, ['id'])
        db.close()
    
    def mark_lazy_content_as_parsed(self, id):
        db = dataset.connect(self.lazy_db_url)
        table = db['generated_content']
        table.update({'id': id, 'is_parsed': True}, ['id'])
        db.close()
    
    
    def update_content_publish_status(self, id, is_published_to_site):
        db = dataset.connect(self.db_url)
        table = db['rewritten_content']
        table.update({'id': id, 'is_published_to_site': is_published_to_site}, ['id'])
        db.close()


    def update_lazy_content_publish_status(self, id, is_published_to_site):
        db = dataset.connect(self.lazy_db_url)
        table = db['llm_generated_content']
        table.update({'id': id, 'is_published_to_site': is_published_to_site}, ['id'])
        db.close()


    def get_content_for_parse(self):
        db = dataset.connect(self.db_url)
        table = db['links']
        result = table.find_one(is_parsed=False)
        db.close()
        return result


    def get_lazy_link_for_parse(self):
        db = dataset.connect(self.lazy_db_url)
        table = db['links']
        result = table.find_one(is_parsed=False)
        db.close()
        return result

    def get_lazy_content_for_parse(self):
        db = dataset.connect(self.lazy_db_url)
        table = db['generated_content']
        result = table.find_one(is_parsed=False)
        db.close()
        return result

    def get_content_for_publish(self):
        db = dataset.connect(self.db_url)
        table = db['rewritten_content']
        result = table.find_one(is_published_to_site=False)
        db.close()
        return result


    def get_lazy_content_for_publish(self):
        db = dataset.connect(self.lazy_db_url)
        table = db['llm_generated_content']
        result = table.find_one(is_published_to_site=False)
        db.close()
        return result


    def write_rewritten_content(
        self, 
        original_content, 
        generated_title, 
        generated_description, 
        rewritten_content, 
        url, 
        og_image_url,
        publish_date,
        is_published_to_site=False):
        db = dataset.connect(self.db_url)
        table = db['rewritten_content']
        table.insert(
            {
                'original_content': original_content, 
                'generated_title': generated_title, 
                'generated_description': generated_description, 
                'rewritten_content': rewritten_content, 
                'url': url, 
                'og_image_url': og_image_url,
                'publish_date': publish_date,
                'is_published_to_site': is_published_to_site
            }
        )
        db.close()


    def write_generated_content(
        self, 
        original_content, 
        generated_title, 
        generated_description, 
        generated_content, 
        url, 
        og_image_url,
        publish_date,
        is_published_to_site=False):
        db = dataset.connect(self.lazy_db_url)
        table = db['llm_generated_content']
        table.insert(
            {
                'original_content': original_content, 
                'generated_title': generated_title, 
                'generated_description': generated_description, 
                'generated_content': generated_content, 
                'url': url, 
                'og_image_url': og_image_url,
                'publish_date': publish_date,
                'is_published_to_site': is_published_to_site
            }
        )
        db.close()

