# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import CrawlSpider
from utilities.start_urls import StartURLs
from utilities.proxy_settings import choose_settings, proxy_settings, charity_engine_settings
from pipelines import MongoDBPipeline
from utilities.cleanUpClass import CleanUp_class


class UpdateSpider(CrawlSpider):
    name = 'update_prodirect'
    allowed_domains = ['prodirectrunning.com']

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        category_name = crawler.settings['category_name']
        spider = super(CrawlSpider, cls(category_name=category_name)).from_crawler(crawler, category_name=category_name)
        spider._follow_links = 'True'
        return spider

    def __init__(self, *args, **kwargs):

        self.category_name = kwargs['category_name']
        start_urls = StartURLs()
        self.start_urls = start_urls.get_start_urls(self.category_name)
        self.cleanUp = CleanUp_class(self.category_name)
        sku_suffix = self.cleanUp.sku_suffix(self.category_name)
        self.MongoDB = MongoDBPipeline(self.category_name)
        self.masterfile_asin_list = self.MongoDB.get_instock_inventory(
            sku_suffix=sku_suffix,
            script_type="update",
            category_name=self.category_name
        )
        super(UpdateSpider, self).__init__()

    def parse_item(self, response):
        print response
        if not response.xpath('//*[@class ="flex-active-slide"]').extract():
            update_item={}

            update_item['Product Code/SKU'] = response.xpath('//*[@id = "content"]//div/@data-quickref').extract_first()
            update_item['Product Name'] = response.xpath('//*[@class="right-column"]/h1/text()').extract_first()
            price_xpath = response.xpath('//*[@class="right-column"]/p[3]/text()').extract_first()
            price = price_xpath.encode('ascii', 'ignore').decode('ascii').strip()
            cost_price = float(price) * 85.00  # converstion_rate = 85.00
            update_item['Price'] = cost_price
            selling_price = cost_price + 500.00 + (cost_price * .15)  # Shipping_Cost = 500.00 , Profit = 15/100
            update_item['Selling Price'] = selling_price
            return update_item


def start_spider():
    start_urls = StartURLs()
    category_name = start_urls.user_input()

    settings = proxy_settings
    settings['category_name'] = category_name
    settings.update(choose_settings())

    process = CrawlerProcess(settings)
    process.crawl(UpdateSpider)
    process.start()


if __name__ == '__main__':
    print "Update Spider"
    start_spider()
