import logging
from uuid import uuid4
from utils.db_agent import DBAgent
from utils.mq_agent import MessageQueueAgent


ACCEPTED_STATUS = "ACCEPTED"
NOTIFICATION_TARGETS_KEY = "notification_targets"
CRAWL_REQUESTS_QUEUE = "crawl_requests"

def ingest(url, notification_targets):
    crawl_id = get_crawl_id()
    mq_agent = MessageQueueAgent()
    mq_agent.publish_message(crawl_id, CRAWL_REQUESTS_QUEUE)
    logging.info("Sent")
    request_data = {"url": url,
                    "crawl_id": crawl_id,
                    "status": ACCEPTED_STATUS}
    if notification_targets is not None:
        request_data[NOTIFICATION_TARGETS_KEY] = notification_targets
    db_agent = DBAgent()
    db_agent.insert_data(request_data)
    logging.info("Inserted to db")
    return crawl_id


def get_crawl_id():
    return str(uuid4())