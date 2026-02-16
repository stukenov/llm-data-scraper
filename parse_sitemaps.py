from sitemap_processor import SitemapProcessor

class ParseSitemaps:

    @staticmethod
    def process_news(url, condition=None, fix_url_func=None, sitemap_sort_type='ASC', url_sort_type='ASC'):
        sitemap_urls = SitemapProcessor.get_sitemaps(url, condition, sitemap_sort_type)
        if not sitemap_urls:
            return None
        last_sitemap_url = sitemap_urls[-1]
        new_urls = SitemapProcessor.get_new_urls_from_sitemap(last_sitemap_url, fix_url_func, url_sort_type)
        if not new_urls:
            return None
        return new_urls[-1]
    
    @staticmethod
    def zakon_condition(loc):
        return loc.endswith('.xml') and loc.split('/')[-1].replace('.xml', '').isdigit()

    @classmethod
    def parse_zakon(cls):
        return cls.process_news("https://www.zakon.kz/sitemap/index.xml", condition=cls.zakon_condition)

    @staticmethod
    def tengrinews_condition(loc):
        return 'sitemap-news' in loc

    @staticmethod
    def tengrinews_fix_url(url):
        replacements = {
            'https://tengrinews.kzhttps://tengrisport.kz/': 'https://tengrisport.kz/',
            'https://tengrinews.kzhttps://tengriauto.kz/': 'https://tengriauto.kz/',
            'https://tengrinews.kz/': 'https://tengrinews.kz/'
        }
        for old, new in replacements.items():
            if url.startswith(old):
                return url.replace(old, new)
        return url

    @classmethod
    def parse_tengrinews(cls):
        tengrinews_urls = SitemapProcessor.get_new_urls_from_sitemap("https://tengrinews.kz/sitemap_ru.xml")
        return tengrinews_urls[0]

    @classmethod
    def parse_nur(cls):
        return cls.process_news("https://www.nur.kz/article-index-sitemap.xml")


    @classmethod
    def parse_informburo(cls):
        return cls.process_news("https://informburo.kz/sitemap.xml", condition=cls.informburo_condition, sitemap_sort_type='DESC')

    @classmethod
    def informburo_condition(cls, loc):
        return 'type=articles' in loc

    @classmethod
    def newtimes_condition(cls, loc):
        return 'sitemap.news' in loc

    @classmethod
    def parse_newtimes(cls):
        return cls.process_news(
            "https://newtimes.kz/sitemap.xml", 
            condition=cls.newtimes_condition, 
            sitemap_sort_type='DESC', 
            url_sort_type='DESC')

    @classmethod
    def parse_golosnaroda(cls):
        return cls.process_news("https://golos-naroda.kz/sitemap.xml", condition=cls.golosnaroda_condition, sitemap_sort_type='DESC', url_sort_type='DESC')

    @classmethod
    def golosnaroda_condition(cls, loc):
        return 'sitemap.news' in loc

    @classmethod
    def parse_almatytv(cls):
        parse_almatytv_links = SitemapProcessor.get_new_urls_from_sitemap("https://almaty.tv/sitemap.news.xml")
        return parse_almatytv_links[0]

    @classmethod
    def parse_lada(cls):
        return cls.process_news("https://www.lada.kz/sitemap.xml", condition=cls.lada_condition, sitemap_sort_type='DESC', url_sort_type='DESC')

    @classmethod
    def lada_condition(cls, loc):
        return 'sitemap.news' in loc

    @classmethod
    def parse_inbusiness(cls):
        parse_inbusiness_links = SitemapProcessor.get_new_urls_from_sitemap("https://inbusiness.kz/gnews-sitemap.xml")
        return parse_inbusiness_links[0]

    @classmethod
    def parse_alau(cls):
        return cls.process_news("https://alau.kz/sitemap.xml", condition=cls.alau_condition, sitemap_sort_type='DESC', url_sort_type='DESC')

    @classmethod
    def alau_condition(cls, loc):
        return 'post-sitemap' in loc

    @classmethod
    def parse_vesti_kz(cls):
        parse_vesti_kz_links = SitemapProcessor.get_new_urls_from_sitemap("https://vesti.kz/sitemap.xml")
        return parse_vesti_kz_links[0]

    @classmethod
    def parse_liter(cls):
        parse_liter_links = SitemapProcessor.get_new_urls_from_sitemap("https://liter.kz/sitemap.news.xml")
        return parse_liter_links[0]

    @classmethod
    def parse_sputnik(cls):
        return cls.process_news("https://ru.sputnik.kz/sitemap_article_index.xml", condition=cls.sputnik_condition, sitemap_sort_type='DESC', url_sort_type='DESC')

    @classmethod
    def sputnik_condition(cls, loc):
        return 'sitemap_article.xml' in loc
