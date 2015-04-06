from PyQt4.QtGui import *
from PyQt4.QtCore import *
import logger
import time
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
        if CURRENTLY_PLAYING['id'] is None:
            logger.error_msg("image_clicked: Playing new song.", None)
            self.play_song()
        else:
            if CURRENTLY_PLAYING['id'] != self.beatmap.id_:
                self.play_song()
            else:
                if time.time() - CURRENTLY_PLAYING['t'] < 10:
                    CURRENTLY_PLAYING['id'] = None
                else:
                    self.play_song()


    def play_song(self):
        CURRENTLY_PLAYING['p'] = self.beatmap.get_song()
        if CURRENTLY_PLAYING['p'] is not None:
            CURRENTLY_PLAYING['p'].play()
            CURRENTLY_PLAYING['id'] = self.beatmap.id_
            CURRENTLY_PLAYING['t'] = time.time()
        else:
            logger.error_msg("play_song: Could not load song of beatmap " + self.beatmap.id_ + ".", None)


class ImageLabel(QLabel):
    def __init__(self, parent=None):
        super(ImageLabel, self).__init__(parent)

    def mousePressEvent(self, event):
        self.emit(SIGNAL("clicked()"))