import pika
import logging
from retry import retry
from src.processor import process


HOST = 'host.docker.internal'
QUEUE_NAME = 'crawl_requests'
# TODO - move these variables into a class
connection_object = None
channel_object = None


def _initialize():
    logging.basicConfig(level=logging.INFO)
    pika_logger = logging.getLogger("pika")
    pika_logger.setLevel(logging.WARNING)
    


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