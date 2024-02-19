import logging
from flask import Flask, request
from app.ingestor import ingest


app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
REQUEST_KEY = "url"


@app.route("/ingest", methods=['POST'])
def base():
    try:
        url = request.form[REQUEST_KEY]
        # TODO - add URL form validation?
    except KeyError:
        logging.exception("Invalid input")
        return {"status": "Invalid input", "message": "should include URL in the body"}, 400
    except:
        logging.exception("An error occured")
        return {"status": "Error", "message": "An error occured"}, 500
    try:
        crawl_id = ingest(url)
        return {"status": "All is ok. Ingested", "crawl_id": crawl_id}, 200
    except:
        logging.exception("An error occured")
        return {"status": "Error", "message": "An error occured"}, 500
