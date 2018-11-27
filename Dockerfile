FROM python:3.7-stretch

RUN mkdir /genericparser
WORKDIR /genericparser

#COPY feedparser-5.2.1.tar.gz .
#COPY kafka-python-1.4.3.tar.gz .
#RUN pip install feedparser-5.2.1.tar.gz kafka-python-1.4.3.tar.gz
RUN pip install kafka-python pymongo bs4

COPY pagebodydao pagebodydao
COPY parseorder parseorder
COPY parseordersource parseordersource
COPY urlsink urlsink

COPY genericparser.py .

ENV KAFKA_BOOTSTRAP_SERVERS kafka:9092
ENV KAFKA_PARSEORDERS_TOPIC parseorders
ENV KAFKA_PARSE_ORDERS_GROUP_ID genericparser
ENV KAFKA_URLS_TOPIC urls

ENV MONGODB_HOST mongo
ENV MONGODB_DB default
ENV MONGODB_RAWPAGES_COLLECTION rawpages
ENV MONGODB_TEXTS_COLLECTION texts
ENV MONGODB_LATESTTEXTS_COLLECTION latesttexts
ENV MONGODB_USERNAME genericparser
ENV MONGODB_PASSWORD genericparser

ENV REGEX_FILTER ^https://www.berlin.de/polizei/polizeimeldungen/.+
