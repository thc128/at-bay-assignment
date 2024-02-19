import logging
from pymongo import MongoClient


HOST = "host.docker.internal"
DB_NAME = "crawls"
REQUESTS_COLLECTION = "crawling_requests"
STATUS_KEY = "status"
RUNNING_STATUS = "RUNNING"
COMPLETE_STATUS = "COMPLETE"
collection_object = None


def get_collection(collection_name=REQUESTS_COLLECTION):
    global collection_object
    if collection_object is None:
        client = MongoClient(HOST)
        db = client[DB_NAME]
        collection_object = db[collection_name]
    return collection_object


def get_status_update_expression(new_status):
    return {"$set": {STATUS_KEY: new_status}}


def get_document_and_update_status(filter_expression, new_status=RUNNING_STATUS):
    update_expression = get_status_update_expression(new_status)
    return get_and_update_document(filter_expression, update_expression)


def update_document_status(filter_expression, new_status):
    update_expression = get_status_update_expression(new_status)
    return update_document(filter_expression, update_expression)


def get_and_update_document(filter_expression, update_expression):
    collection = get_collection()
    result = collection.find_one_and_update(filter_expression, update_expression)
    logging.info(f"Result: {result}")
    return result


def update_document(filter_expression, update_expression):
    collection = get_collection()
    result = collection.update_one(filter_expression, update_expression)
    logging.info(f"Updated")
    return result