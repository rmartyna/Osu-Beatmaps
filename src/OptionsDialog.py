from PyQt4.QtGui import *
from PyQt4.QtCore import *
import logger
import images


class OptionsDialog(QDialog):
    def __init__(self, parent=None):
        super(OptionsDialog, self).__init__(parent)

        logger.error_msg("__init__: Started OptionsDialog.", None)

        self.setWindowTitle("Options")
        self.setWindowIcon(images.get_icon())