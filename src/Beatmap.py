import os
from PyQt4.QtGui import *
import pydub
from init import *
import logger
import images


class Beatmap:
    def __init__(self, id_, all_maps, index):
        self.id_ = id_
        self.all_maps = all_maps
        self.index = index
        self.json = None
        self.creator = None
        self.profile = None
        self.user_page = None
        self.artist = None
        self.title = None
        self.name = None
        self.image = None
        self.song = None

    def get_name(self):
        if self.name is None:
            try:
                self.artist = ARTIST_.search(self.json).group(1)
            except (AttributeError, IndexError) as err:
                logger.error_msg('get_name: Could not find artist of beatmap ' + self.id_ + '.', err)
                self.artist = 'DEFAULT'
            try:
                self.title = TITLE_.search(self.json).group(1)
            except (AttributeError, IndexError) as err:
                logger.error_msg('get_name: Could not find title of baetmap ' + self.id_ + '.', err)
                self.title = 'DEFAULT'
            try:
                self.name = INVALID_CHARACTERS_.sub('', str(self.id_) + ' ' + self.artist + ' - ' + self.title)
            except Exception as err:
                logger.error_msg('get_name: Could not convert beatmap name to windows-like. Artist: '
                                 + self.artist + ' ,title: ' + self.title + '.', err)
                self.name = 'DEFAULT - DEFAULT'
        return self.name

    def get_image(self):
        if self.image is None:
            try:
                if not os.path.exists("temp/" + self.id_ + ".jpg"):
                    raise Exception("Could not find image.")
                self.image = QImage()
                self.image.load("temp/" + self.id_ + '.jpg')
            except Exception:
                logger.error_msg("get_image: Could not load image of beatmap " + self.id_ + ".", None)
                try:
                    self.image = images.get_default_image()
                except Exception as err:
                    logger.error_msg("get_image: Could not load default beatmap image.", err)
        return self.image

    def get_song(self):
        if self.song is None:
            try:
                pydub.AudioSegment.from_mp3("temp/" + self.id_ + '.mp3').export("temp/" + self.id_ +
                                                                                '.wav', format='wav')
                try:
                    self.song = QSound("temp/" + self.id_ + '.wav')
                except Exception:
                    logger.error_msg("get_song: Could not find wav song of beatmap " + self.id_ + ".", None)
            except Exception as err:
                logger.error_msg("get_song: Could not load mp3 and convert to wav.", err)
        return self.song

    def add_to_database(self):
        try:
            DATABASE.add(self.id_)
            pickle.dump(DATABASE, open("database.dat", "wb"))
        except Exception as err:
            logger.error_msg('add_to_database: Could not dump database.', err)