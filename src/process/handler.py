import logging
from src.processor import process
from utils.mq_agent import get_channel, add_consumer, start_consuming


def _initialize():
    logging.basicConfig(level=logging.INFO)
    

def callback(ch, method, properties, body):
    logging.info(f"Received {body}")
    process(body.decode())
    

def handler():
    channel = get_channel()
    logging.info("Starting consumer")
    add_consumer(channel, callback)
    start_consuming(channel)
    # connection.close()


if __name__ == '__main__':
    _initialize()
    handler()