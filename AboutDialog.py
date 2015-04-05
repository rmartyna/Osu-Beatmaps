from PyQt4.QtGui import *
from PyQt4.QtCore import *
from init import *
import logger
import images


class AboutDialog(QDialog):

    def __init__(self, parent=None):
        super(AboutDialog, self).__init__(parent)

        logger.error_msg("__init__: Started AboutDialog.", None)

        label = QLabel("""<b>Osu Beatmaps!</b> v. {0}
        <p>Last updated: {1}</p>
        <p>This application is used to help filter
        beatmaps,<br/>allowing you to download high quality
        maps automatically.</p>
        <p>You can contact me at: {2}</p>
        <p>More information and source code at:<br/>
         {3}</p>""".format(VERSION, DATE,
                                   EMAIL, GITHUB), self)
        self.button = QPushButton("OK")
        self.button.setMaximumWidth(100)

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.button, 0, Qt.AlignCenter)
        self.setLayout(layout)

        self.connect(self.button, SIGNAL("clicked()"), self, SLOT("accept()"))

        self.setWindowTitle("About")
        self.setWindowIcon(images.get_icon())

        logger.error_msg("__init__: Finished AboutDialog.", None)
