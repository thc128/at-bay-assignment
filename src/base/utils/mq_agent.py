import pika
import logging
from retry import retry


HOST = "host.docker.internal"
QUEUE_NAME = "crawl_requests"
pika_logger = logging.getLogger("pika")
pika_logger.setLevel(logging.WARNING)
# TODO - move these variables into a class
connection_object = None
channel_object = None


def get_connection():
    global connection_object
    if connection_object is None:
        connection_object = pika.BlockingConnection(pika.ConnectionParameters(HOST))
    return connection_object


@retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 3))
def get_channel(queue_name=QUEUE_NAME):
    global channel_object
    if channel_object is None:
        connection = get_connection()
        channel_object = connection.channel()
        channel_object.queue_declare(queue=queue_name)
    return channel_object


def publish_message(channel, message, queue=QUEUE_NAME):
    channel.basic_publish(exchange='',
                            routing_key=queue,
                            body=message)


def add_consumer(channel, callback_function, queue=QUEUE_NAME):
    channel.basic_consume(queue=queue,
                        auto_ack=True,
                        on_message_callback=callback_function)
    

def start_consuming(channel):
    channel.start_consuming()