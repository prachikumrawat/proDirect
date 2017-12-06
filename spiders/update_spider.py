# -*- coding: utf-8 -*-
import csv
import os
import sys
from scrapy.http import Request
sys.path.append('../')
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import CrawlSpider
from utilities.start_urls import StartURLs
from utilities.proxy_settings import choose_settings, proxy_settings

class UpdateSpider(CrawlSpider):
    name = 'update_prodirect'
    allowed_domains = ['prodirectrunning.com']

    def start_requests(self):
        for url in self.start_urls:
            request = Request(url, callback=self.parse_update)
            yield request

    def __init__(self):
        super(UpdateSpider, self).__init__()
        start_urls = StartURLs()
        self.start_urls = start_urls.read_urls()
#     #     product_url_list = []
#     #
#     #     file_path = os.path.realpath('../utilities/bin/output/prodirect_running.csv')
#     #     with open(file_path, 'r') as update_spider_file:
#     #         for row in csv.DictReader(update_spider_file):
#     #             if row['Product URL'] not in product_url_list:
#     #                 print row['Product URL']
#     #                 product_url_list.append(row['Product URL'])
#     #
#     #             yield product_url_list
#
#
#     @classmethod
#     def from_crawler(cls, crawler, *args, **kwargs):
#         category_name = crawler.settings['category_name']
#         spider = super(CrawlSpider, cls(category_name=category_name)).from_crawler(crawler, category_name=category_name)
#         spider._follow_links = 'True'
#         return spider
#     #
#     # def __init__(self, *args, **kwargs):
#     #     super(UpdateSpider, self).__init__()
#     #     # self.category_name = kwargs['category_name']
#
#     def start_requests(self):
#         start_urls = StartURLs()
#         update_urls_list = start_urls.read_urls()
#         print update_urls_list
#
#         for item_url in update_urls_list:
#             request = Request(item_url, callback=self.parse)
#             print request
#             yield request
#     #     start_urls = StartURLs()
#     #     update_items_urls = start_urls.read_urls()
#     #     for item in update_items_urls:
#     #         request = Request(item.url, callback=self.parse)
#     #         print request
#     #         yield request
#

    def parse_update(self, response):

        update_dict = {}
        update_dict['Product Code/SKU'] = response.xpath(
            '//*[@id = "content"]//div/@data-quickref').extract_first()
        price_xpath = response.xpath('//*[@class="right-column"]/p[3]/text()').extract_first()
        price = price_xpath.encode('ascii', 'ignore').decode('ascii').strip()
        cost_price = float(price) * 85.00  # converstion_rate = 85.00
        update_dict['Cost Price'] = cost_price
        selling_price = cost_price + 500.00 + (cost_price * .15)  # Shipping_Cost = 500.00 , Profit = 15/100
        update_dict['Selling Price'] = float(selling_price)

        return update_dict

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
    print "Spider"
    start_spider()
#
#
# def start_spider():
#     start_urls = StartURLs()
#     update_urls_list = start_urls.read_urls()
#     print update_urls_list
#     #
#     # for item_url in update_urls_list:
#     #     request = Request(item_url, callback=self.parse)
#     #     print request
#     #     yield request
#
#     settings = proxy_settings
#     # # settings['category_name'] = category_name
#     # # settings.update(choose_settings())
#     #
#     process = CrawlerProcess(settings)
#     process.crawl(UpdateSpider)
#     process.start()
# #
# #
# if __name__ == '__main__':
#     start_spider()
#     # settings = proxy_settings
#     # process = CrawlerProcess(settings)
#     # process.crawl(UpdateSpider)
#     # process.start()

