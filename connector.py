import requests
from init import *
import logger


def login(username, password):
    LOGIN_DATA['username'] = username
    LOGIN_DATA['password'] = password
    SESSION.post(LOGIN_URL, data=LOGIN_DATA)
    LOGIN_DATA['username'] = None
    LOGIN_DATA['password'] = None


def check_if_logged():
    try:
        response = SESSION.get(MAIN_PAGE_URL).content
        try:
            LOGIN_PAGE_.search(response).group(1)
            return True
        except (AttributeError, IndexError):
            return False
    except requests.RequestException as err:
        logger.error_msg('check_if_logged: Could not connect with Osu! site.', err)
        return False


def reset_connection():
    global SESSION
    SESSION.close()
    SESSION = requests.Session()
    check_if_logged()
