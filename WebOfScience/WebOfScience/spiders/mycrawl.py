import scrapy
from WebOfScience.items import WebofscienceItem


class MySpider(scrapy.Spider):
    name = 'myspider'
    allowed_domains = []
    start_urls = []

    def parse(self, response):
        pass
