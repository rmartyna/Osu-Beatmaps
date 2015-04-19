from PyQt4.QtGui import QIcon, QImage
import logger

CALLED = False


def load():
    global ICON, DEFAULT_IMAGE
    logger.error_msg("load: Called first time.", None)
    ICON = QIcon("res/icon.png")
    DEFAULT_IMAGE = QImage("res/default.jpg")


def get_icon():
    global CALLED
    logger.error_msg("get_icon: Returning icon.", None)
    if not CALLED:
        CALLED = True
        load()
    return ICON


def get_default_image():
    global CALLED
    if not CALLED:
        CALLED = True
        load()
    return DEFAULT_IMAGE