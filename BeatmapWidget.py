from PyQt4.QtGui import *
from PyQt4.QtCore import *
import logger


class BeatmapWidget(QWidget):
    def __init__(self, parent=None):
        super(BeatmapWidget, self).__init__(parent)

        logger.error_msg("__init__: Started BeatmapWidget.", None)

        self.add_buttons()
        self.setMinimumHeight(100)

        logger.error_msg("__init__: Finished BeatmapWidget.", None)

    def add_buttons(self):
        self.layout = QHBoxLayout()

        self.button1 = QPushButton("Button 1")
        self.layout.addWidget(self.button1)

        self.label1 = QLabel("label 1")
        self.layout.addWidget(self.label1)

        self.setLayout(self.layout)