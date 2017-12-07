# -*- coding: utf-8 -*-

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
