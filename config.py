import logging
import requests
import os

from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

load_dotenv()

TEST = False

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)
HANDLER = RotatingFileHandler('flask_call_list_upload.log', maxBytes=2 * 1024 * 1024, backupCount=2)
HANDLER.setFormatter(logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s :: %(lineno)d'))
LOGGER.addHandler(HANDLER)

API_LOGIN = os.environ.get("API_LOGIN")
API_PASSWORD = os.environ.get("API_PASSWORD")
URL_BASE = os.environ.get("URL_BASE")
URL_AUTH = URL_BASE + os.environ.get("URL_AUTH")
URL_GENERAL = URL_BASE + os.environ.get("URL_GENERAL")
URL_QUEUE_LOADER = os.environ.get("URL_QUEUE_LOADER")

AGENTS = ("Agent1", "Agent2", "Agent3", "Agent4", "Agent5")

UUIDS = {
    "Agent1": os.environ.get("Agent1"),
    "Agent2": os.environ.get("Agent2"),
    "Agent3": os.environ.get("Agent3"),
    "Agent4": os.environ.get("Agent4"),
    "Agent5": os.environ.get("Agent5")
}

INITIALS = os.environ.get("INITIALS")


def send_tg(message, type_msg="error"):
    to_send_error = os.environ.get("to_send_error")
    to_send_ok = os.environ.get("to_send_ok")
    to_send = to_send_error if type_msg == "error" else to_send_ok
    error_token = os.environ.get("error_token")
    info_token = os.environ.get("info_token")
    bot_token = error_token if type_msg == "error" else info_token
    for dev_id in to_send:
        send_message = ('flask_call_list_upload\n'
                        f'{message}')
        url = ('https://api.telegram.org/'
               f'{bot_token}/'
               f'sendMessage?chat_id={dev_id}&text={send_message}')
        payloads = {}
        headers = {}
        try:
            requests.get(url=url, headers=headers, data=payloads)
        except Exception as send_tg_reponse_error:
            LOGGER.info(send_tg_reponse_error)
    return
