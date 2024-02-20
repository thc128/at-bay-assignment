import logging
from pymongo import MongoClient
from utils.constants import HOST, DB_NAME, COLLECTION_NAME, \
                            STATUS_KEY, RUNNING_STATUS


class DBAgent():
    def __init__(self) -> None:
        self.client = MongoClient(HOST)
        self.db = self.client[DB_NAME]
        self.collection = self.db[COLLECTION_NAME]

    def insert_data(self, data):
        result = self.collection.insert_one(data)
        logging.info(f"Inserted object {data}.")

    def get_document_and_update_status(self, filter_expression, new_status=RUNNING_STATUS):
        update_expression = {"$set": {STATUS_KEY: new_status}}
        return self.get_and_update_document(filter_expression, update_expression)

    def get_and_update_document(self, filter_expression, update_expression):
        result = self.collection.find_one_and_update(filter_expression, update_expression)
        logging.info(f"Result: {result}")
        return result
    
    def update_document(self,filter_expression, update_expression):
        result = self.collection.update_one(filter_expression, update_expression)
        logging.info(f"Updated")
        return result
    
    def get_document(self, id):
        filter_expression = {"crawl_id": id}
        result = self.collection.find_one(filter_expression)
        logging.info(f"Result: {result}.")
        return result
