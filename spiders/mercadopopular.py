#!/usr/bin/env python3

from scrapy.http import Request, HtmlResponse
from scrapy.spiders import Spider
from scrapy.linkextractors import LinkExtractor
import dateutil.parser as dparser

from texts import Post

AUTHOR_XPATH = "//span[@class='post-meta']/a[@rel='author']/text()"
TITLE_XPATH = "//meta[@property='og:title']/@content"
DATE_XPATH = "//span[@class='post-meta']/text()"
BODY_XPATH = "//div[@class='post-entry']//p//text()"

class MercadoPopularSpider(Spider):

    name = 'mercadopopular'
    allowed_domains = ['mercadopopular.org']
    start_urls = ['http://mercadopopular.org']
    link_extractor = LinkExtractor(unique=True, allow=r'\d{4}/\d{2}/.*/$')   
    
    def parse(self, response):
        """
        Parse a blog post and all requests to follow
        """
        
        post = self._get_post(response)
        r = [post]
        r.extend(self._extract_requests(response))
        return r


    def _extract_requests(self, response):
        """
        Gets requests from a page
        """

        requests = []
        if isinstance(response, HtmlResponse):
            links = self.link_extractor.extract_links(response)
            requests.extend(Request(link.url, callback=self.parse)
                            for link in links)
        return requests

    
    def _get_post(self, response):
        """
        Creates a representation of the blog post.
        """
        
        item = Post(url=response.url)

        self._set_title(item, response)
        self._set_body(item, response)
        self._set_metadata(item, response)
        
        return item

    
    def _set_title(self, page, response):
        """
        Grabs the title.
        """

        if isinstance(response, HtmlResponse):
            title = response.xpath(TITLE_XPATH).extract()
            if title:
                page['title'] = title[0]


    def _set_metadata(self, page, response):

        if isinstance(response, HtmlResponse):
            author = response.xpath(AUTHOR_XPATH).extract()
            date = response.xpath(DATE_XPATH).extract()
            date = ' '.join(date)
            
            if author:
                page['author'] = author[0]
            if date:
                page['date'] = dparser.parse(date, dayfirst=True,
                                             fuzzy=True).isoformat()


    def _set_body(self, page, response):
        """
        Grabs the main text of a post.
        """

        if isinstance(response, HtmlResponse):
            body = response.xpath(BODY_XPATH).extract()
            if body:
                page['body'] = body
