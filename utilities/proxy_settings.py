import sys
import time


proxy_settings = {

    'BOT_NAME': 'Googlebot',
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0',
    'AUTOTHROTTLE_ENABLED': True,
    'AUTOTHROTTLE_DEBUG': True,
    'AUTOTHROTTLE_MAX_DELAY': 1,
    'AUTOTHROTTLE_START_DELAY': 0.1,
    'AUTOTHROTTLE_TARGET_CONCURRENCY': 60,
    'RETRY_TIMES': 10,
    'RETRY_AFTER': 600,
    'DOWNLOAD_TIMEOUT': 100,
    'CONCURRENT_REQUESTS': 100,
    'CONCURRENT_REQUESTS_PER_DOMAIN': 100,
    'AJAXCRAWL_ENABLED': True,
    'ITEM_PIPELINES': {'pipelines.MongoDBPipeline': 100},

}

storm_proxy_settings = {
    'DOWNLOADER_MIDDLEWARES': {'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,},
    'ITEM_PIPELINES': {'pipelines.MongoDBPipeline': 100},
    'CONCURRENT_REQUESTS': 30,
    'CONCURRENT_REQUESTS_PER_DOMAIN': 20,
    'DOWNLOAD_DELAY': 5,
    'AUTOTHROTTLE_ENABLED': True,
    'COOKIES_ENABLED': True
}
crawlera_proxy_settings = {
    'DOWNLOADER_MIDDLEWARES': {'scrapy_crawlera.CrawleraMiddleware': 300},
    'CRAWLERA_ENABLED': True,
    'CRAWLERA_APIKEY': '00bc5d0e8cb54879b3816fc395cac46b',
    'CRAWLERA_URL': 'http://proxy.crawlera.com:8010',
    'DOWNLOAD_DELAY':5,
    'CRAWLERA_DOWNLOAD_TIMEOUT': 190,
    'RETRY_ENABLED'  : True,
    'AUTOTHROTTLE_ENABLED': False,
    'CONCURRENT_REQUESTS': 30,
    'CONCURRENT_REQUESTS_PER_DOMAIN': 30,
}

charity_engine_settings = {
    'DOWNLOADER_MIDDLEWARES': {'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,},
    'ITEM_PIPELINES': {'pipelines.MongoDBPipeline': 100},
    'CONCURRENT_REQUESTS': 100,
    'CONCURRENT_REQUESTS_PER_DOMAIN': 100,
    'DOWNLOAD_DELAY': 0.5,
    'AUTOTHROTTLE_ENABLED': False,
}

def choose_settings():

    proxy_choice = int(raw_input('Choose one: \n1. Storm Proxy\n2. Crawlera\n3. Charity Engine:\n '))
    if proxy_choice == 1:
        return storm_proxy_settings
    elif proxy_choice == 2:
        return crawlera_proxy_settings
    elif proxy_choice == 3:
        return charity_engine_settings
    else:
        print "Incorrect choice! The script will now terminate, please rerun and choose a valid choice"
        time.sleep(5)
        sys.exit("Script terminated")
