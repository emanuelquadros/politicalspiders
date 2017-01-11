from base_polspider import BasePolSpider
from scrapy.linkextractors import LinkExtractor

class MidiaSemMascara(BasePolSpider):

    name = 'midiasemMascara'
    
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        
        self.AUTHOR_XPATH = "//meta[@name='title']/@content"
        self.TITLE_XPATH = "//meta[@property='og:title']/@content"
        self.DATE_XPATH = "//span[@class='created']/text()"
        self.BODY_XPATH = "//div[@class='article']//p[not(@class='articleinfo')]//text()"
        
        self.allowed_domains = ['midiasemmascara.org']
        self.start_urls = ['http://www.midiasemmascara.org/']
        self.link_extractor = LinkExtractor(unique=True, allow=r'/\d+.*.html')
