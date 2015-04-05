from PyQt4.QtGui import *
from PyQt4.QtCore import *
import logger

class MyMainWidget(QWidget):

    def __init__(self, parent=None):
        super(MyMainWidget, self).__init__(parent)

        logger.error_msg("__init__: Started MyMainWidget.", None)

        self.add_buttons()

        logger.error_msg("__init__: Finished MyMainWidget.", None)

    def add_buttons(self):
        self.layout = QVBoxLayout()

        self.button1 = QPushButton("Button 1")
        self.layout.addWidget(self.button1)

        self.label1 = QLabel()
        self.layout.addWidget(self.label1)

        self.setLayout(self.layout)