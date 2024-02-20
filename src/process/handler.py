import logging
from src.processor import process
from utils.mq_agent import MessageQueueAgent


CRAWL_REQUESTS_QUEUE = "crawl_requests"


def _initialize():
    logging.basicConfig(level=logging.INFO)
    

def callback(ch, method, properties, body):
    try:
        logging.info(f"Received {body}")
        process(body.decode())
    except:
        logging.exception("An error occured")


def handler():
    mq_agent = MessageQueueAgent()
    logging.info("Starting consumer")
    mq_agent.add_consumer(callback, CRAWL_REQUESTS_QUEUE)
    mq_agent.start_consuming()


if __name__ == '__main__':
    _initialize()
    handler()