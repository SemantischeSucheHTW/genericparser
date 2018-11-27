from bs4 import BeautifulSoup
from pagebodydao import MongoDBDao
from parseordersource import KafkaSource
from urlsink import KafkaSink

import os
import re
import urllib

def env(key):
    value = os.environ.get(key)
    if not value:
        raise f"{key} not set!!!"
    return value

pageorderSource = KafkaSource({
  "topic": env("KAFKA_PARSEORDERS_TOPIC"),
  "bootstrap_servers": env("KAFKA_BOOTSTRAP_SERVERS"),
  "group_id": env("KAFKA_PARSE_ORDERS_GROUP_ID")
})

pagebodyDao = MongoDBDao({
  "host": env("MONGODB_HOST"),
  "db": env("MONGODB_DB"),
  "rawpages_collection": env("MONGODB_RAWPAGES_COLLECTION"),
  "texts_collection": env("MONGODB_TEXTS_COLLECTION"),
  "latesttexts_collection": env("MONGODB_LATESTTEXTS_COLLECTION"),
  "username": env("MONGODB_USERNAME"),
  "password": env("MONGODB_PASSWORD"),
  "authSource": env("MONGODB_DB")
})

urlsink = KafkaSink({
  "topic": env("KAFKA_URLS_TOPIC"),
  "bootstrap_servers": env("KAFKA_BOOTSTRAP_SERVERS"),
})

print(env("REGEX_FILTER"))

err = None
while not err:
    order = pageorderSource.getOrder()
    print(f"Got order {order}")
    (err, body) = pagebodyDao.retrieveBody(order)
    if (err):
        break
    soup = BeautifulSoup(body, "html.parser")
    for script in soup(["script", "head"]):
        script.decompose()
    text = '\n'.join(soup.stripped_strings)
    err = pagebodyDao.storeText(order, text)
    print(f"Text stored for {order}")

    parse_res = urllib.parse.urlparse(order.url)
    base_url = f"{parse_res.scheme}://{parse_res.netloc}"

    link_urls = [ link.get('href') for link in soup.find_all('a') ]

    for link_url in link_urls:
        if not re.match("https?", link_url):
            link_url = base_url + link_url
        if re.search(env("REGEX_FILTER"), link_url):
            print(f"New url found: {link_url}")
            urlsink.send(link_url)

print(f"ERROR during write: {err}")
