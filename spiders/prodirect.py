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
from utilities.csv_pipeline import CsvPipeline


class ProdirectSpider(CrawlSpider):
    name = 'prodirect'
    allowed_domains = ['prodirectrunning.com']

    def start_requests(self):
        for url in self.start_urls:
            if isinstance(url, tuple):
                category_page = url
                request = Request(category_page, callback=self.parse_category)
                yield request
            else:
                for start_url in self.start_urls:
                    request = Request(start_url, callback=self.parse_category)
                    yield request

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        category_name = crawler.settings['category_name']
        spider = super(CrawlSpider, cls(category_name=category_name)).from_crawler(crawler, category_name=category_name)
        spider._follow_links = 'True'
        return spider

    def __init__(self, *args, **kwargs):

        super(ProdirectSpider, self).__init__()
        self.category_name = kwargs['category_name']
        start_urls = StartURLs()
        self.start_urls = start_urls.get_start_urls(self.category_name)
        self.cleanUp = CleanUp_class(self.category_name)
        sku_suffix = self.cleanUp.sku_suffix(self.category_name)
        self.MongoDB = MongoDBPipeline(self.category_name)
        self.masterfile_asin_list = self.MongoDB.get_instock_inventory(
            sku_suffix=sku_suffix,
            script_type="replenishment",
            category_name=self.category_name
        )

    def parse_category(self, response):
        print response
        products = LinkExtractor(restrict_xpaths='//*[@class="item"]').extract_links(response)
        for product in products:
            if product.url:
                request = Request(product.url, callback=self.parse_item)
                yield request
        next_page = response.xpath('//*[@class ="next-page"]/a/@href').extract_first()
        if next_page:
            yield Request(url='http://www.prodirectrunning.com/'+next_page, callback=self.parse_category)

    def parse_item(self, response):
        print response
        if not response.xpath('//*[@class ="flex-active-slide"]').extract():
            item = {}
            item['Product Code/SKU'] = response.xpath('//*[@id = "content"]//div/@data-quickref').extract_first()
            item['Product Name'] = response.xpath('//*[@class="right-column"]/h1/text()').extract_first()
            price_xpath = response.xpath('//*[@class="right-column"]/p[3]/text()').extract_first()
            price = price_xpath.encode('ascii', 'ignore').decode('ascii').strip()
            cost_price = float(price) * 85.00  #converstion_rate = 85.00
            item['Cost Price'] = cost_price
            selling_price = cost_price + 500.00 + (cost_price * .15) # Shipping_Cost = 500.00 , Profit = 15/100
            item['Selling Price'] = selling_price
            item['Product URL'] = response.url
            if response.xpath("//*[@id='content']/div/div[4]/div[1]/div/ul/li[1]"):
                description = response.xpath("//*[@id='content']/div/div[4]/div[1]/div/div[2]/div[1]/text()").extract()
                item['Description'] = ''.join(description).strip()

            images_xpath = response.xpath("//*[@class='product-slider-holder']//li/img/@src").extract()
            item['Product Image1'] = 'http://www.prodirectrunning.com/'+images_xpath[0]
            item['Product Image2'] = 'http://www.prodirectrunning.com/'+images_xpath[1]

            size_list = response.xpath('//*[@name="size"]/option/@value').extract()[1:]
            if list('OUT OF STOCK') in size_list:
                pass
            else:
                for size in size_list:
                    item['Size'] = size

            # indexes = [1, 2]
            # for index, image in zip(images_xpath, indexes):
            #     image_name = image
            #     item['Product Image-{}'.format(index)] = image_name
            #     if index == 2:
            #         break
            # for index, image in enumerate(images_xpath, 1):
            #     item['Product Image-{}'.format(index)] = image
            #     if index == 3:
            #         break
            # for image in images_xpath:
            #     print 'http://www.prodirectrunning.com/'+image

            item['Quantity'] = 5
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
