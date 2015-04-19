import time
import threading
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from init import *
import logger
import downloader
import connector


class BeatmapWidget(QWidget):
    def __init__(self, beatmap, item, parent=None):
        super(BeatmapWidget, self).__init__(parent)

        self.container = parent
        self.item = item
        self.beatmap = beatmap

        self.imageLabel = ImageLabel()
        self.imageLabel.setPixmap(QPixmap.fromImage(self.beatmap.get_image()))
        self.imageLabel.setMinimumSize(160, 120)
        self.nameLabel = QLabel(self.beatmap.get_name())
        self.download_button = QPushButton("Download")
        self.remove_button = QPushButton("Remove")

        self.layout = QGridLayout()
        self.layout.addWidget(self.imageLabel, 0, 0, 2, 2)
        self.layout.addWidget(self.nameLabel, 0, 2, 2, 6)
        self.layout.addWidget(self.download_button, 0, 8, 1, 2)
        self.layout.addWidget(self.remove_button, 1, 8, 1, 2)
        self.setLayout(self.layout)

        self.connect(self.imageLabel, SIGNAL("clicked()"), self.image_clicked)
        self.connect(self.download_button, SIGNAL("clicked()"), self.download_beatmap_wraper)
        self.connect(self.remove_button, SIGNAL("clicked()"), self.remove_beatmap_wrapper)
        self.connect(self, SIGNAL("remove_beatmap()"), self.remove_beatmap)

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

    def download_beatmap_wraper(self):
        if connector.check_if_logged():
            thread = threading.Thread(target=BeatmapWidget.download_beatmap, args=(self,))
            thread.start()
        else:
            QMessageBox.information(self, "Could not download map.", "You should login first.")

    def download_beatmap(self):
        downloader.download_beatmap(self.beatmap)
        self.emit(SIGNAL("remove_beatmap()"))

    def remove_beatmap_wrapper(self):
        self.beatmap.add_to_database()
        self.emit(SIGNAL("remove_beatmap()"))

    def remove_beatmap(self):
        self.container.delete_widget(self.item)


class ImageLabel(QLabel):
    def __init__(self, parent=None):
        super(ImageLabel, self).__init__(parent)

    def mousePressEvent(self, event):
        self.emit(SIGNAL("clicked()"))