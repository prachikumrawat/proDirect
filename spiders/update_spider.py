# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import CrawlSpider
from utilities.start_urls import StartURLs
from utilities.proxy_settings import choose_settings, proxy_settings, charity_engine_settings
from pipelines import MongoDBPipeline
from utilities.cleanUpClass import CleanUp_class


class ProdirectSpider(CrawlSpider):
    name = 'prodirect'
    allowed_domains = ['prodirectrunning.com']

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
            script_type="update",
            category_name=self.category_name
        )

    def parse(self):
        pass


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
    print "Update Spider"
    start_spider()
