import logging
from flask import Flask, request
from app.db_agent import get_document

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
CRAWL_ID_KEY = "crawl_id"


@app.route("/status", methods=['POST'])
def status_handler():
    try:
        crawl_id = request.form[CRAWL_ID_KEY]
        # TODO - add CRAWL ID validation?
    except KeyError:
        logging.exception("Invalid input")
        return {"status": "Invalid input",
                 "message": "should include crawl ID in the body"}, 400
    except:
        logging.exception("An error occured")
        return {"status": "Error", "message": "An error occured"}, 500
    try:
        response = get_response(crawl_id)
        return response, 200
    except:
        logging.exception("An error occured")
        return {"status": "Error", "message": "An error occured"}, 500


def get_response(id):
    result = get_document(id)
    status = "NOT_FOUND" if result is None else result.get("status")
    response = {"status": status, "crawl_id": id}
    if status == "COMPLETE":
        response["file_location"] = result.get("file_location")
    return response