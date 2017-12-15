# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
import logging
import pymongo

class MongoDBPipeline(object):
    """ Save an item to MongoDB """
    collection_name = 'products'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
    
    @classmethod
    def from_crawler(cls, crawler):
        # pull in information from settings.py
        return cls(
            mongo_uri = crawler.settings.get('MONGO_URI'),
            mongo_db = crawler.settings.get('MONGO_DATABASE')
        )
    
    def open_spider(self, spider):
        # initializing spider
        # opening db connection
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
    
    def close_spider(self, spider):
        # clean up when spider is closed
        self.client.close()
    
    def process_item(self, item, spider):
        """ Looks for a duplicate. If it isn't found it
            inserts the document, otherwise it drops it. """
        # looks for a duplicate
        duplicate_check = self.db[self.collection_name].find({'name': item['name'], 'store': item['store'], 'category': item['category'], 'animal': item['animal']}).count()
        if duplicate_check == 0:
            self.db[self.collection_name].insert(dict(item))
            logging.debug('Product added to MongoDB')
            return item
        else:
            # logging.debug('Duplicate found. Skipping product')
            raise DropItem('Duplicate found. Skipping product: %s' % item['name'])
        # return item

# class DuplicatesPipeline(object):
#     """ Looks for duplicates of items that were already processed """
#     def __init__(self):
#         self.ids_seen = set()

#     def process_item(self, item, spider):
#         if item['id'] in self.ids_seen:
#             raise DropItem("Duplicate item found: %s" % item)
#         else:
#             self.ids_seen.add(item['id'])
#             return item
