import pika
import logging
from retry import retry
from src.processor import process


HOST = 'host.docker.internal'
QUEUE_NAME = 'crawl_requests'
# TODO - move these variables into a class
connection = None
channel = None


def _initialize():
    logging.basicConfig(level=logging.INFO)
    pika_logger = logging.getLogger("pika")
    pika_logger.setLevel(logging.WARNING)
    


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


def callback(ch, method, properties, body):
    logging.info(f"Received {body}")
    process(body.decode())
    


def handler():
    channel = get_channel()
    channel.queue_declare(queue=QUEUE_NAME)
    logging.info("Starting consumer")
    channel.basic_consume(queue=QUEUE_NAME,
                        auto_ack=True,
                        on_message_callback=callback)
    channel.start_consuming()
    # connection.close()


if __name__ == '__main__':
    _initialize()
    handler()