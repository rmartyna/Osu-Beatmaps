from PyQt4.QtGui import *
from PyQt4.QtCore import *
import logger
import images


class ExitDialog(QDialog):

    def __init__(self, parent=None):
        super(ExitDialog, self).__init__(parent)

        logger.error_msg("__init__: Started ExitDialog.", None)

        label = QLabel("Are you sure you want to exit?")
        self.yesButton = QPushButton("Yes")
        self.noButton = QPushButton("No")

        layout = QGridLayout()
        layout.addWidget(label, 0, 0, 1, 2)
        layout.addWidget(self.yesButton, 1, 0)
        layout.addWidget(self.noButton, 1, 1)
        self.setLayout(layout)

        self.connect(self.yesButton, SIGNAL("clicked()"), self, SLOT("accept()"))
        self.connect(self.noButton, SIGNAL("clicked()"), self, SLOT("reject()"))

        self.setWindowTitle("Logout")
        self.setWindowIcon(images.get_icon())

        logger.error_msg("__init__: Finished ExitDialog.", None)