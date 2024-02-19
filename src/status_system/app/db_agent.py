import logging
from pymongo import MongoClient


HOST = "host.docker.internal"
DB_NAME = "crawls"
REQUESTS_COLLECTION = "crawling_requests"
STATUS_KEY = "status"
collection_object = None


def get_collection(collection_name=REQUESTS_COLLECTION):
    global collection_object
    if collection_object is None:
        client = MongoClient(HOST)
        db = client[DB_NAME]
        collection_object = db[collection_name]
    return collection_object


def get_document(id):
    collection = get_collection()
    filter_expression = {"crawl_id": id}
    result = collection.find_one(filter_expression)
    logging.info(f"Result: {result}.")
    return result