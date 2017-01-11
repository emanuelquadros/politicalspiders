from base_polspider import BasePolSpider
from scrapy.linkextractors import LinkExtractor

class InstitutoLiberal(BasePolSpider):

    name = 'institutoliberal'
    
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        
        self.AUTHOR_XPATH = "(//span[@class='fn'])[1]//text()"
        self.TITLE_XPATH = "//meta[@property='og:title']/@content"
        self.DATE_XPATH = "//meta[@property='article:published_time']/@content"
        self.BODY_XPATH = "//div[@class='entry-content']//p//text()"
        
        self.allowed_domains = ['institutoliberal.org.br']
        self.start_urls = ['https://www.institutoliberal.org.br/blog/']
        self.link_extractor = LinkExtractor(unique=True, allow=r'blog/.*/$')
