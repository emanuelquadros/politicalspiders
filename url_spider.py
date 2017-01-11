#!/usr/bin/env python3

from scrapy.selector import HtmlXPathSelector
from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor
import os
import argparse

parser = argparse.ArgumentParser(description='web crawler')
parser.add_argument('domain_name', help='Domain name to be crawled')

args = parser.parse_args()

DOMAIN = args.domain_name
URL = 'http://%s' % DOMAIN
links = []

class PolSpider(Spider):

    name = 'polspider'
    allowed_domains = [DOMAIN]
    start_urls = [URL]

    def parse(self, response):

        html = sel.select("//body//text()")

        # Getting list of links for ref
        le = LinkExtractor(unique=True)
        for link in le.extract_links(response):
            links.append(link.url)
            yield Request(link.url, callback=self.parse)

            
if __name__ == "__main__":
            
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    process.crawl(PolSpider)
    process.start()

    if not os.path.exists(DOMAIN):
        os.makedirs(DOMAIN)

    out_path = DOMAIN + '/links'

    with open(out_path, 'w') as out_file:
        for url in links:
            print(url, file=out_file)
