from PyQt4.QtGui import *
from PyQt4.QtCore import *


class MyMainWidget(QWidget):

    def __init__(self, parent=None):
        super(MyMainWidget, self).__init__(parent)

        self.add_buttons()

    def add_buttons(self):
        self.layout = QVBoxLayout()

        self.button1 = QPushButton("Button 1")
        self.layout.addWidget(self.button1)

        self.label1 = QLabel()
        self.layout.addWidget(self.label1)

        self.setLayout(self.layout)