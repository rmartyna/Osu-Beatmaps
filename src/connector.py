from init import *
import logger


def login(username, password):
    logger.error_msg("login: Started login.", None)

    LOGIN_DATA['username'] = username
    LOGIN_DATA['password'] = password
    SESSION.post(LOGIN_URL, data=LOGIN_DATA)
    LOGIN_DATA['username'] = None
    LOGIN_DATA['password'] = None

    logger.error_msg("login: Finished login.", None)


def check_if_logged():
    logger.error_msg("check_if_logged: Started check if logged.", None)
    try:
        response = SESSION.get(MAIN_PAGE_URL).content
        try:
            LOGIN_PAGE_.search(response).group(1)
            logger.error_msg("check_if_logged: Found username, returning True.", None)
            return True
        except (AttributeError, IndexError):
            logger.error_msg("check_if_logged: Could not find username, returning False.", None)
            return False
    except requests.RequestException as err:
        logger.error_msg('check_if_logged: Could not connect with Osu! site.', err)
        return False


def reset_connection():
    global SESSION
    logger.error_msg("reset_connection: Started reset connection.", None)
    SESSION.close()
    SESSION = requests.Session()
    logger.error_msg("reset_connection: Checking if logged.", None)
    check_if_logged()
