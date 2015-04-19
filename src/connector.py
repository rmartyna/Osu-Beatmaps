from init import *
import logger


def login(username, password):
    logger.error_msg("login: Started login.", None)

    LOGIN_DATA['username'] = username
    LOGIN_DATA['password'] = password
    SESSION[0].post(LOGIN_URL, data=LOGIN_DATA)
    LOGIN_DATA['username'] = None
    LOGIN_DATA['password'] = None


def check_if_logged():
    logger.error_msg("check_if_logged: Started check if logged.", None)

    try:
        response = SESSION[0].get(MAIN_PAGE_URL).content
        try:
            LOGIN_PAGE_USERNAME_.search(response).group(1)
            return True
        except (AttributeError, IndexError):
            return False
    except requests.RequestException as err:
        logger.error_msg('check_if_logged: Could not connect with Osu! site.', err)
        return False


def reset_connection():
    logger.error_msg("reset_connection: Started reset connection.", None)

    SESSION[0] = requests.Session()
