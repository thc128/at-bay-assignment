import logging
from src.notifier import notify
from utils.mq_agent import get_channel, add_consumer, start_consuming


def _initialize():
    logging.basicConfig(level=logging.INFO)
    

def callback(ch, method, properties, body):
    try:
        logging.info(f"Received {body}")
        notify(body.decode())
    except:
        logging.exception("An error occured")
    

def handler():
    channel = get_channel(queue_name="notifications")
    logging.info("Starting consumer")
    add_consumer(channel, callback, queue="notifications")
    start_consuming(channel)
    # connection.close()


if __name__ == '__main__':
    _initialize()
    handler()