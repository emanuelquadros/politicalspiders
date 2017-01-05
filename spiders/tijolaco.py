#!/usr/bin/env python3

from scrapy.http import Request, HtmlResponse
from scrapy.spiders import Spider
from scrapy.linkextractors import LinkExtractor
import dateutil.parser as dparser

from texts import Post


class TijolacoSpider(Spider):

    name = 'tijolaco'
    allowed_domains = ['tijolaco.com.br']
    start_urls = ['http://www.tijolaco.com.br/blog']
    link_extractor = LinkExtractor(unique=True, allow=r'blog/.*/$',
                                   deny=['blog/voltamos/'
                                         , 'blog/author/'
                                         , 'blog/tag/'
                                         , 'blog/category/'
                                         , 'blog/regras-de-uso/'
                                         , 'blog/eu-quero-ajudar/'
                                         , 'blog/voltamos/'
                                         , 'blog/contato/'])
   
    
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
            title = response.xpath("//meta[@property='og:title']/@content").extract()
            if title:
                page['title'] = title[0]


    def _set_metadata(self, page, response):

        if isinstance(response, HtmlResponse):
            author = response.xpath("//a[@rel='author']/text()").extract()
            date = response.xpath("//p[@class='post-byline']/text()").extract()
            
            if author:
                page['author'] = author[0]
            if date:
                page['date'] = dparser.parse(date[1], dayfirst=True,
                                             fuzzy=True).isoformat()


    def _set_body(self, page, response):
        """
        Grabs the main text of a post.
        """

        if isinstance(response, HtmlResponse):
            body = response.xpath("//div[@class='entry-inner']//text()").extract()
            if body:
                page['body'] = body
