from base_polspider import BasePolSpider
from scrapy.linkextractors import LinkExtractor

class SolidariedadeSocialistaSpider(BasePolSpider):

    name = 'solidariedade_socialista'
    
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        
        # messy blog - AUTHOR_XPATH will always be null for this one.
        self.AUTHOR_XPATH = "//span[@class='post-meta']/a[@rel='author']/text()"
        self.TITLE_XPATH = "//meta[@property='og:title']/@content"
        self.DATE_XPATH = "//link[@rel='canonical']/@href"
        self.BODY_XPATH = ("//div[@id='content']/div/p[not(@class='info') "
                           "and not(@id='filedunder') and position()<last()]//text()")
    
        self.allowed_domains = ['solidariedadesocialista.wordpress.com']
        self.start_urls = ['http://solidariedadesocialista.wordpress.com/']
        self.link_extractor = LinkExtractor(unique=True,
                                       allow=r'\d{4}/\d{2}/.*/$')
