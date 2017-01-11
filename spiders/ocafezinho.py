from base_polspider import BasePolSpider
from scrapy.linkextractors import LinkExtractor

class OCafezinho(BasePolSpider):

    name = 'ocafezinho'
    
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        
        self.AUTHOR_XPATH = "//a[@rel='author']/text()"
        self.TITLE_XPATH = "//meta[@property='og:title']/@content"
        self.DATE_XPATH = "//meta[@property='article:published_time']/@content"
        self.BODY_XPATH = "//div[@class='maincontent']//p[not(ancestor::div[@class='info'])]//text()"
        
        self.allowed_domains = ['www.ocafezinho.com']
        self.start_urls = ['http://www.ocafezinho.com/']
        self.link_extractor = LinkExtractor(unique=True, allow=r'/\d{4}/\d{2}/\d{2}/.+/$')
