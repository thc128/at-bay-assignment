import pika
import json
import logging
from retry import retry
from uuid import uuid4

HOST = 'host.docker.internal'
QUEUE_NAME = 'crawl_requests'
pika_logger = logging.getLogger("pika")
pika_logger.setLevel(logging.WARNING)
connection = None
channel = None


def get_connection():
    if connection:
        return connection
    return pika.BlockingConnection(pika.ConnectionParameters(HOST))


@retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 3))
def get_channel():
    if channel:
        return channel
    connection = get_connection()
    return connection.channel()


def ingest(url):
    channel = get_channel()
    channel.queue_declare(queue=QUEUE_NAME)
    crawl_id = get_crawl_id()
    message_body = {"url": url,
                    "crawl_id": crawl_id}
    channel.basic_publish(exchange='',
                            routing_key=QUEUE_NAME,
                            body=json.dumps(message_body))
    logging.info("Sent")
    return crawl_id
    # connection.close()


def get_crawl_id():
    return str(uuid4())