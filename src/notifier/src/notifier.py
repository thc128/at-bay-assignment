import json
import logging


def email_notifier(email_address, message):
    logging.info(f"Sending email notification to {email_address} for {message}")


def slack_user_notifier(user_name, message):
    logging.info(f"Sending slack user notification to {user_name} for {message}")


def slack_channel_notifier(channel_name, message):
    logging.info(f"Sending slack channel notification to {channel_name} for {message}")


NOTIFIERS_MAPPING = {"email": email_notifier,
                     "slack_user": slack_user_notifier,
                     "slack_channel": slack_channel_notifier}


def notify(message):
    logging.info(f"Notifier called with this message: {message}")
    message_data = json.loads(message)
    notification_targets = message_data.get("notification_targets")
    for target in notification_targets:
        if target not in NOTIFIERS_MAPPING:
            logging.warning(f"Notification for {target} is not supported")
            continue
        notifier_function = NOTIFIERS_MAPPING[target]
        notification_target_value = notification_targets[target]
        notifier_function(notification_target_value, message)