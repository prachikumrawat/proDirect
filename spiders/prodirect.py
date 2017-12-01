# -*- coding: utf-8 -*-
import sys
import time
sys.path.append('../')
import scrapy
import random
from scrapy.crawler import CrawlerProcess
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from items import ProdirectrunningItem
from utilities.start_urls import StartURLs
from utilities.proxy_settings import choose_settings, proxy_settings, charity_engine_settings
from pipelines import MongoDBPipeline
from utilities.cleanUpClass import CleanUp_class

class ProdirectSpider(CrawlSpider):
    name = 'prodirect'
    allowed_domains = ['prodirectrunning.com']

    def declare_xpath(self):
        self.getAllListXpath = "//*[@class='list']//a/@href"
        self.getAllProductXpath = "//*[@class='item']/a/@href"

    def start_requests(self):
        for url in self.start_urls:
            # yield scrapy.Request(url, dont_filter=True)
            request = Request(url, callback=self.parse_category, dont_filter=True)
            request.meta['Category'] = 'Null'
            print request
            yield request

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        category_name = crawler.settings['category_name']
        spider = super(CrawlSpider, cls(category_name=category_name)).from_crawler(crawler, category_name=category_name)
        spider._follow_links = 'True'
        return spider

    def __init__(self, *args, **kwargs):

        self.declare_xpath()
        self.category_name = kwargs['category_name']
        start_urls = StartURLs()
        self.start_urls = start_urls.get_start_urls(self.category_name)
        # print self.start_urls
        self.cleanUp = CleanUp_class(self.category_name)
        sku_suffix = self.cleanUp.sku_suffix(self.category_name)
        self.MongoDB = MongoDBPipeline(self.category_name)
        print self.MongoDB
        self.masterfile_asin_list = self.MongoDB.get_instock_inventory(
            sku_suffix=sku_suffix,
            script_type="replenishment",
            category_name=self.category_name
        )
        super(ProdirectSpider, self).__init__()

    def parse_category(self, response):

        print response
        products = LinkExtractor(restrict_xpaths='//*[@class="item"]').extract_links(response)
        for product in products:
            if product.url:
                request = Request(product.url, callback=self.parse_item, priority=random.choice(range(-2, 2)))
                yield request
        next_page = response.xpath('//*[@class ="next-page"]/a/@href').extract_first()
        print next_page
        if next_page:
             yield Request(url='http://www.prodirectrunning.com/'+next_page, callback=self.parse_category)

    def parse_item(self, response):
        print response
        item = ProdirectrunningItem()
        hxs = HtmlXPathSelector(response)
        item['product_name'] = hxs.select('//*[@id="define-profile"]/h1/text()').extract()
        item['description'] = hxs.select(
         '//*[@id="content"]/div/div[4]/div[1]/div/div[2]/div[1]/text()').extract()
        item['price'] = hxs.select('//*[@id="define-profile"]/p[3]/text()').extract_first()
        item['product_url'] = response.url

        return item


def start_spider():
    start_urls = StartURLs()
    category_name = start_urls.user_input()

    settings = proxy_settings
    settings['category_name'] = category_name
    settings.update(choose_settings())

    process = CrawlerProcess(settings)
    process.crawl(ProdirectSpider)
    process.start()


if __name__ == '__main__':
    print "Spider"
    start_spider()
