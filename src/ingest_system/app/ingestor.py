import logging
from uuid import uuid4
from utils.db_agent import insert_data
from utils.mq_agent import get_channel, publish_message


ACCEPTED_STATUS = "ACCEPTED"


def ingest(url):
    crawl_id = get_crawl_id()
    channel = get_channel()
    publish_message(channel, crawl_id)
    logging.info("Sent")
    request_data = {"url": url,
                    "crawl_id": crawl_id,
                    "status": ACCEPTED_STATUS}
    insert_data(request_data)
    logging.info("Inserted to db")
    return crawl_id
    # connection.close()


def get_crawl_id():
    return str(uuid4())