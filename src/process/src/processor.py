import json
import logging
import requests
import os
from utils.db_agent import DBAgent
from utils.mq_agent import MessageQueueAgent
from utils.constants import ERROR_STATUS, COMPLETE_STATUS,\
                            DOWNLOADS_BASE_FOLDER, NOTIFICATION_TARGETS_KEY,\
                            NOTIFICATIONS_QUEUE


def process(crawl_id):
    logging.info(f"Processing {crawl_id}")
    db_agent = DBAgent()
    request_data = db_agent.get_document_and_update_status(crawl_id)
    if request_data is None:
        logging.warning("Did not find relevant data")
        return
    logging.info(f"URL: {request_data.get("url")}")
    download_status, location = download_page(request_data.get("url"), crawl_id)
    status = COMPLETE_STATUS if download_status else ERROR_STATUS
    final_update_expression = {"$set": {"status": status, "file_location": location}}
    db_agent.update_document(crawl_id, final_update_expression)
    logging.info("DB updated")
    notification_targets = request_data.get(NOTIFICATION_TARGETS_KEY)
    if notification_targets is None:
        return
    message = {"status": status,
                "crawl_id": crawl_id,
                "file_location": location,
                "notification_targets": notification_targets}
    mq_agent = MessageQueueAgent()
    mq_agent.publish_message(json.dumps(message), NOTIFICATIONS_QUEUE)

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