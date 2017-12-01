# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import time
import sys
from pymongo import MongoClient
from scrapy.exceptions import DropItem
# from utilities.write_csv import WriteCSV

# from scrapy.conf import settings
from pprint import pprint

class MongoDBPipeline(object):
    collection_name = 'Mens_Running'

    def __init__(self, category_name, **kwargs):
        self.category_name = category_name
        self.client = MongoClient('mongodb://localhost:27107/')
        self.db_name = 'Prodirect_Running'
        self.bulk_insert_dict = {}
        self.db_connect()

    @classmethod
    def from_crawler(cls, crawler):
        category_name = crawler.settings['category_name']
        db_name = crawler.settings['MONGODB_DB']
        if db_name:
            return cls(category_name, db_name=db_name)
        else:
            return cls(category_name)

    def open_spider(self, spider):
        print 'Opening..'
        client = MongoClient('mongodb://localhost:27107/')
        print client
        # self.output_file = open('../utilities/bin/Output/prodirect_running.csv', 'w+b')

        db = client[self.db_name]
        print db
        # self.db[self.category_name].drop()

    def close_spider(self, spider):
        # WriteCSV(self.output_file)
        # self.output_file.close()
        # client = MongoClient('mongodb://localhost:27017/')
        self.client.close()
        print 'closing..'

    def db_connect(self):
        client = MongoClient('mongodb://localhost:27017/')
        db = client[self.db_name]
        collection = db[self.category_name]
        print collection
        # if self.collection in self.db:
        #     if 'y' in raw_input('Erase previous data for {} (Y/N): '.format(self.category_name)).lower():
        #         self.collection.drop()

    def process_item(self, itemp, spider):
        # client = MongoClient('mongodb://localhost:27017/')
        # self.db = client[self.db_name]
        # self.collection = client[self.db[self.category_name]]

        self.db_name[self.collection_name].insert(dict(itemp))
        return itemp

    def get_instock_inventory(self, sku_suffix, script_type, category_name, **kwargs):
        client = MongoClient('mongodb://localhost:27017/')
        master_db = client['Prodirect_Running']
        if category_name == "Mens Running":
            masterfile = master_db['Mens_Running']
        elif category_name == "Running":
            masterfile = master_db['Running']
        else:
            print "Incorrect choice! The script will now terminate, please rerun and choose a valid choice"
            time.sleep(5)
            sys.exit("Script terminated")

        if script_type == "update":
            regex_query = '.*-{}.*'.format(sku_suffix)
            cursor = masterfile.find({'$and': [{'quantity': {'$ne': '0'}},
                                               {'quantity': {'$ne': 0}},
                                               {'sku': {'$regex': regex_query}}
                                               ]})

        elif script_type == "replenishment":
            cursor = masterfile.find()

        if kwargs.get('API_Update'):
            asin_list = []
            updated_inventory = {document['asin']: '' for document in self.collection.find({})}
            print 'Previously updated asins {}'.format(len(updated_inventory))

            for document in cursor:
                if not updated_inventory.get(document['asin']):
                    asin_list.append(document['asin'])
                else:
                    del (updated_inventory[document['asin']])

            print 'Running Updates for {} asins'.format(len(asin_list))
            return tuple(asin_list)

        else:
            masterfile_asin_list = []
            for row in cursor:
                masterfile_asin_list.append(row['asin'].strip())
            return masterfile_asin_list


class DuplicatesPipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, itemp, spider):
        if itemp['id'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % itemp)
        else:
            self.ids_seen.add(itemp['id'])
            return itemp