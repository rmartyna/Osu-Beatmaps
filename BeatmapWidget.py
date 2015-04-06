from PyQt4.QtGui import *
from PyQt4.QtCore import *
import logger


class BeatmapWidget(QWidget):
    def __init__(self, beatmap, parent=None):
        super(BeatmapWidget, self).__init__(parent)

        logger.error_msg("__init__: Started BeatmapWidget.", None)

        self.add_widgets(beatmap)

        logger.error_msg("__init__: Finished BeatmapWidget.", None)

    def add_widgets(self, beatmap):
        self.layout = QGridLayout()

        self.imageLabel = QLabel()
        self.imageLabel.setPixmap(QPixmap.fromImage(beatmap.get_picture()))
        self.imageLabel.setMinimumSize(160, 120)
        self.nameLabel = QLabel(beatmap.get_name())
        self.layout.addWidget(self.imageLabel, 0, 0, 1, 2)
        self.layout.addWidget(self.nameLabel, 0, 2, 1, 8)

        self.setLayout(self.layout)