import json
import logging
from utils.db_agent import get_document_and_update_status, update_document


ERROR_STATUS = "ERROR"
COMPLETE_STATUS = "COMPLETE"


def process(crawl_id):
    logging.info(f"Processing {crawl_id}")
    request_data = get_document_and_update_status({"crawl_id": crawl_id})
    if request_data is None:
        logging.warning("Did not find relevant data")
        return
    logging.info(f"URL: {request_data.get("url")}")
    download_status, location = download_page(request_data.get("url"))
    status = COMPLETE_STATUS if download_status else ERROR_STATUS
    final_update_expression = {"$set": {"status": status, "file_location": location}}
    update_document({"crawl_id": crawl_id}, final_update_expression)
    logging.info("DB updated")


def download_page(url):
    try:
        logging.info("Downloading page")
        file_location = ""
        logging.info(f"Page downloaded. File location: {file_location}")
        return True, file_location
    except:
        return False, ""