import logging
from src.notifier import notify
from utils.mq_agent import MessageQueueAgent


def _initialize():
    logging.basicConfig(level=logging.INFO)
    

def callback(ch, method, properties, body):
    try:
        logging.info(f"Received {body}")
        notify(body.decode())
    except:
        logging.exception("An error occured")
    

def handler():
    mq_agent = MessageQueueAgent()
    logging.info("Starting consumer")
    mq_agent.add_consumer(callback, queue="notifications")
    mq_agent.start_consuming()


if __name__ == '__main__':
    _initialize()
    handler()