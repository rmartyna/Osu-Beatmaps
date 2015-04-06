from PyQt4.QtGui import *
from PyQt4.QtCore import *
import logger
import pydub
from init import *


class BeatmapWidget(QWidget):
    def __init__(self, beatmap, parent=None):
        super(BeatmapWidget, self).__init__(parent)

        logger.error_msg("__init__: Started BeatmapWidget.", None)

        self.beatmap = beatmap
        self.add_widgets()


        logger.error_msg("__init__: Finished BeatmapWidget.", None)

    def add_widgets(self):
        self.layout = QGridLayout()

        self.imageLabel = ImageLabel()
        self.imageLabel.setPixmap(QPixmap.fromImage(self.beatmap.get_picture()))
        self.imageLabel.setMinimumSize(160, 120)
        self.nameLabel = QLabel(self.beatmap.get_name())
        self.layout.addWidget(self.imageLabel, 0, 0, 1, 2)
        self.layout.addWidget(self.nameLabel, 0, 2, 1, 8)

        self.connect(self.imageLabel, SIGNAL("clicked()"), self.image_clicked)

        self.setLayout(self.layout)

    def image_clicked(self):
        logger.error_msg("image_clicked: Start of function.", None)
        if CURRENTLY_PLAYING['p'] is not None:
            logger.error_msg("image_clicked: Stopping last song.", None)
            CURRENTLY_PLAYING['p'].stop()
        if CURRENTLY_PLAYING['id'] != self.beatmap.id_:
            logger.error_msg("image_clicked: Playing new song.", None)
            CURRENTLY_PLAYING['p'] = self.beatmap.get_song().play()
            CURRENTLY_PLAYING['id'] = self.beatmap.id_


class ImageLabel(QLabel):
    def __init__(self, parent=None):
        super(ImageLabel, self).__init__(parent)

    def mousePressEvent(self, event):
        self.emit(SIGNAL("clicked()"))