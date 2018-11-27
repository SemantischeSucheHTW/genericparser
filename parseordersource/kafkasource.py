from kafka import KafkaConsumer
from parseordersource import ParseOrderSource
from parseorder import ParseOrder
import json
import datetime

class KafkaSource(ParseOrderSource):

    '''
    Provides continouus stream of ParseOrder objects to
    be processed from Kafka
    '''

    def _parseRawPageData(bytes):
        base = json.loads(bytes.decode('utf-8'))
        base['datetime'] = datetime.datetime.fromisoformat(base['datetime'])
        return ParseOrder(**base)

    def __init__(self, config):

        
        '''
        Setup an instance of KafkaSource
        :param **config: Configuration passed to KafkaConsumer
        '''
        config["key_deserializer"] = lambda k: k.decode('utf-8')
        config["value_deserializer"] = KafkaSource._parseRawPageData
        topic = config.pop("topic")
        self.consumer = KafkaConsumer(topic, **config)

    def getOrder(self):
        kv = next(self.consumer)
        assert isinstance(kv.value, ParseOrder)
        return kv.value
