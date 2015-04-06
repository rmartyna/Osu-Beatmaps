from init import *
from PyQt4.QtGui import QImage
from PyQt4.QtGui import QSound
import logger
from pydub import AudioSegment


class Beatmap:
    def __init__(self, id_):
        self.id_ = id_
        self.source = None
        self.json = None
        self.creator = None
        self.profile = None
        self.user_page = None
        self.artist = None
        self.title = None
        self.name = None
        self.picture = None
        self.song = None

    def get_name(self):
        logger.error_msg("get_name: Getting name of beatmap " + self.id_ + ".", None)
        if self.name is None:
            logger.error_msg("get_name: Name is None. Calculating name.", None)
            try:
                self.artist = ARTIST_.search(self.json).group(1)
            except (AttributeError, IndexError) as err:
                logger.error_msg('beatmap_name: Could not find artist of beatmap ' + self.id_ + '.', err)
                self.artist = 'DEFAULT'
            try:
                self.title = TITLE_.search(self.json).group(1)
            except (AttributeError, IndexError) as err:
                logger.error_msg('beatmap_name: Could not find title of baetmap ' + self.id_ + '.', err)
                self.title = 'DEFAULT'
            try:
                self.name = INVALID_CHARACTERS_.sub('', str(self.id_) + ' ' + self.artist + ' - ' + self.title)
            except Exception as err:
                logger.error_msg('beatmap_name: Could not convert beatmap name to windows-like. Artist: '
                                 + self.artist + ' ,title: ' + self.title + '.', err)
                self.name = 'DEFAULT - DEFAULT'
        return self.name

    def get_picture(self):
        logger.error_msg("get_image: Getting picture of beatmap: " + self.id_ + '.', None)
        if self.picture is None:
            logger.error_msg("get_image: Picture is None. Opening picture.", None)
            try:
                self.picture = QImage()
                self.picture.load("temp/" + self.id_ + '.jpg')
            except Exception as err:
                logger.error_msg("get_image: Could not load beatmap picture.", err)
                try:
                    self.picture = QImage()
                    self.picture.load("resources/default.jpg")
                except Exception as err:
                    logger.error_msg("get_image: Could not load default beatmap picture.", err)
        return self.picture

    def get_song(self):
        logger.error_msg("get_song: Getting song of beatmap: " + self.id_ + ".", None)
        if self.song is None:
            logger.error_msg("get_song: Song is None. Loading song.", None)
            try:
                AudioSegment.from_mp3("temp/" + self.id_ + '.mp3').export("temp/" + self.id_ + '.wav', format='wav')
                try:
                    self.song = QSound("temp/" + self.id_ + '.wav')
                except Exception as err:
                    logger.error_msg("get_song: Could not find wav song.", err)
            except Exception as err:
                logger.error_msg("get_song: Could not load mp3 and convert to wav.", err)
        return self.song