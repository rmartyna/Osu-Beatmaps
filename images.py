from PyQt4.QtGui import QIcon
import logger

CALLED = False

def load():
    global ICON
    logger.error_msg("load: Called first time.", None)
    ICON = QIcon("icon.png")

def get_icon():
    global CALLED
    logger.error_msg("get_icon: Returning icon.", None)
    if not CALLED:
        CALLED = True
        load()
    return ICON