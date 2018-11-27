from pagebodydao import PageBodyDao
from pymongo import MongoClient

import datetime

class MongoDBDao(PageBodyDao):

    def __init__(self, config):

        '''
        Setup an instance of MongoDBDao.
        Keys in config are: host, port, database, collection
        :param config: dict with keys
        '''
        c_copy =  dict(config)
        db = c_copy.pop('db')
        rawpages_collection = c_copy.pop('rawpages_collection')
        texts_collection = c_copy.pop('texts_collection')
        latesttexts_collection = c_copy.pop('latesttexts_collection')

        self.client = MongoClient(**c_copy)
        self.db = self.client[db]
        self.rawpages_collection = self.db[rawpages_collection]
        self.texts_collection = self.db[texts_collection]
        self.latesttexts_collection = self.db[latesttexts_collection]

    def retrieveBody(self, parseOrder):

        doc = self.rawpages_collection.find_one(f"{parseOrder.url};{parseOrder.datetime.isoformat()}")
        if (not doc):
            return ("Did not find RawPageData associated with the given ParseOrder", None)

        body = doc["body"]

        return (None, body)

    def storeText(self, parseOrder, text):

        isodatetime = parseOrder.datetime.isoformat()
        entry = {
                '_id': f"{parseOrder.url};{isodatetime}",
                'url': parseOrder.url,
                'datetime': isodatetime,
                'text': text
        }
        self.texts_collection.insert_one(entry)

        update = {
                'datetime': isodatetime,
                'text': text
        }
        self.latesttexts_collection.update_one(
                filter={'_id': parseOrder.url},
                update={'$set': update},
                upsert=True
        )

        print(f"New entry to {parseOrder.url} written")

        return None
