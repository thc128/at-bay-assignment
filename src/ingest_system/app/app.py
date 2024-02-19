import json
import logging
from flask import Flask, request
from app.ingestor import ingest


app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
REQUEST_KEY = "url"
NOTIFICATION_TARGETS_KEY = "notification_targets"

@app.route("/ingest", methods=['POST'])
def base():
    try:
        request_data = request.get_json(force=True)
        url = request_data[REQUEST_KEY]
        notification_targets = request_data.get(NOTIFICATION_TARGETS_KEY)
    except KeyError:
        logging.exception("Invalid input")
        return {"status": "Invalid input", "message": "should include URL in the body"}, 400
    except:
        logging.exception("An error occured")
        return {"status": "Error", "message": "An error occured"}, 500
    try:
        crawl_id = ingest(url, notification_targets)
        return {"status": "All is ok. Ingested", "crawl_id": crawl_id}, 200
    except:
        logging.exception("An error occured")
        return {"status": "Error", "message": "An error occured"}, 500
