from urlsink.urlsink import URLSink
from kafka import KafkaProducer

class KafkaSink(URLSink):
    def __init__(self, config):
        config["key_serializer"] = str.encode
        config["value_serializer"] = str.encode
        c_copy = dict(config)
        topic = c_copy.pop("topic")
        self.producer = KafkaProducer(**c_copy)
        self.topic = topic

    def send(self, url):
        future = self.producer.send(self.topic, key=url, value=url)
        future.get(timeout=10)
