#!/usr/bin/env python3

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import argparse

parser = argparse.ArgumentParser(description='web crawler')
parser.add_argument('spider', help='name of the spider to use')
args = parser.parse_args()

process = CrawlerProcess(get_project_settings())

process.crawl(args.spider)
process.start()
