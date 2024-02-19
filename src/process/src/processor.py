import json
import logging
import requests
import os
from utils.db_agent import get_document_and_update_status, update_document
from utils.mq_agent import get_channel, publish_message


ERROR_STATUS = "ERROR"
COMPLETE_STATUS = "COMPLETE"
DOWNLOADS_BASE_FOLDER = "downloaded_pages"
NOTIFICATION_TARGETS_KEY = "notification_targets"


def process(crawl_id):
    logging.info(f"Processing {crawl_id}")
    request_data = get_document_and_update_status({"crawl_id": crawl_id})
    if request_data is None:
        logging.warning("Did not find relevant data")
        return
    logging.info(f"URL: {request_data.get("url")}")
    download_status, location = download_page(request_data.get("url"), crawl_id)
    status = COMPLETE_STATUS if download_status else ERROR_STATUS
    final_update_expression = {"$set": {"status": status, "file_location": location}}
    update_document({"crawl_id": crawl_id}, final_update_expression)
    logging.info("DB updated")
    notification_targets = request_data.get(NOTIFICATION_TARGETS_KEY)
    if notification_targets is None:
        return
    message = {"status": status,
                "crawl_id": crawl_id,
                "file_location": location,
                "notification_targets": notification_targets}
    channel = get_channel(queue_name="notifications")
    publish_message(channel, json.dumps(message), "notifications")

def download_page(url, id):
    try:
        logging.info("Downloading page")
        file_name = ".".join([id, "html"])
        file_location = os.path.join(DOWNLOADS_BASE_FOLDER, file_name)
        with open(file_location, 'w') as output_file:
            content = requests.get(url)
            output_file.write(content.text)
        logging.info(f"Page downloaded. File location: {file_location}")
        return True, file_location
    except:
        logging.exception("Download failed")
        return False, ""