import json
import logging


def process(body):
    logging.info(f"Processing {body}")
    message = json.loads(body)
    logging.info(f"URL: {message.get("url")}")