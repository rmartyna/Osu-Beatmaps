from PyQt4.QtGui import *
from PyQt4.QtCore import *
import logger
import time
import downloader
from init import *


class BeatmapWidget(QWidget):
    def __init__(self, beatmap, item, parent=None):
        super(BeatmapWidget, self).__init__(parent)

        self.container = parent
        self.item = item
        self.beatmap = beatmap
        self.add_widgets()

    def add_widgets(self):
        self.layout = QGridLayout()

        self.imageLabel = ImageLabel()
        self.imageLabel.setPixmap(QPixmap.fromImage(self.beatmap.get_picture()))
        self.imageLabel.setMinimumSize(160, 120)
        self.nameLabel = QLabel(self.beatmap.get_name())
        self.download_button = QPushButton("Download")
        self.layout.addWidget(self.imageLabel, 0, 0, 1, 2)
        self.layout.addWidget(self.nameLabel, 0, 2, 1, 6)
        self.layout.addWidget(self.download_button, 0, 8, 1, 2)

        self.connect(self.imageLabel, SIGNAL("clicked()"), self.image_clicked)
        self.connect(self.download_button, SIGNAL("clicked()"), self.download_beatmap)

        self.setLayout(self.layout)

    def image_clicked(self):
        if CURRENTLY_PLAYING['p'] is not None:
            CURRENTLY_PLAYING['p'].stop()
        if CURRENTLY_PLAYING['id'] is None:
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

    def download_beatmap(self):
        downloader.download_beatmap(self.beatmap)
        self.container.delete_widget(self.item)


class ImageLabel(QLabel):
    def __init__(self, parent=None):
        super(ImageLabel, self).__init__(parent)

    def mousePressEvent(self, event):
        self.emit(SIGNAL("clicked()"))