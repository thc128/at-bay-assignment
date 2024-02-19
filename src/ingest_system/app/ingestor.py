import logging
from uuid import uuid4
from utils.db_agent import insert_data
from utils.mq_agent import get_channel, publish_message


ACCEPTED_STATUS = "ACCEPTED"
NOTIFICATION_TARGETS_KEY = "notification_targets"


def ingest(url, notification_targets):
    crawl_id = get_crawl_id()
    channel = get_channel()
    publish_message(channel, crawl_id)
    logging.info("Sent")
    request_data = {"url": url,
                    "crawl_id": crawl_id,
                    "status": ACCEPTED_STATUS}
    if notification_targets is not None:
        request_data[NOTIFICATION_TARGETS_KEY] = notification_targets
    insert_data(request_data)
    logging.info("Inserted to db")
    return crawl_id


def get_crawl_id():
    return str(uuid4())