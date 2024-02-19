import logging
from pymongo import MongoClient


HOST = "host.docker.internal"
DB_NAME = "crawls"
COLLECTION_NAME = "crawling_requests"
collection_object = None

def get_collection():
    global collection_object
    if collection_object is None:
        client = MongoClient(HOST)
        db = client[DB_NAME]
        collection_object = db[COLLECTION_NAME]
    return collection_object


def insert_data(data):
    collection = get_collection()
    result = collection.insert_one(data)
    logging.info(f"Inserted object {data}.")