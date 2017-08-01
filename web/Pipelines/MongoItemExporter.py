import pymongo
from web.settings import MONGO_URL, MONGO_DATABASE


class MongoPipeline(object):
    collection_name = 'scrapy_items'

    def __init__(self):
        self.mongo_uri = MONGO_URL
        self.mongo_db = MONGO_DATABASE

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.collection = self.db[self.collection_name]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        item = dict(item)
        try:
            if not item['title'] or not item['link']:
                return item
        except:
            return
        try:
            self.collection.remove({'link': item['link']})
        except:
            pass
        item['site'] = spider.name
        self.collection.insert(item)
        return item
