HOST = "host.docker.internal"
DOWNLOADS_BASE_FOLDER = "downloaded_pages"
DB_NAME = "crawls"
COLLECTION_NAME = "crawling_requests"

# keys
STATUS_KEY = "status"
URL_KEY = "url"
NOTIFICATION_TARGETS_KEY = "notification_targets"
CRAWL_ID_KEY = "crawl_id"

#statuses
RUNNING_STATUS = "RUNNING"
COMPLETE_STATUS = "COMPLETE"
ACCEPTED_STATUS = "ACCEPTED"
ERROR_STATUS = "ERROR"


#queues
CRAWL_REQUESTS_QUEUE = "crawl_requests"
NOTIFICATIONS_QUEUE = "notifications"
