import pika
import json
import logging
from retry import retry
from uuid import uuid4
from utils.db_agent import insert_data


HOST = "host.docker.internal"
QUEUE_NAME = "crawl_requests"
ACCEPTED_STATUS = "ACCEPTED"
pika_logger = logging.getLogger("pika")
pika_logger.setLevel(logging.WARNING)
connection_object = None
channel_object = None


def get_connection():
    global connection_object
    if connection_object is None:
        connection_object = pika.BlockingConnection(pika.ConnectionParameters(HOST))
    return connection_object


@retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 3))
def get_channel():
    global channel_object
    if channel_object is None:
        connection = get_connection()
        channel_object = connection.channel()
    return channel_object


def ingest(url):
    channel = get_channel()
    channel.queue_declare(queue=QUEUE_NAME)
    crawl_id = get_crawl_id()
    channel.basic_publish(exchange='',
                            routing_key=QUEUE_NAME,
                            body=crawl_id)
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