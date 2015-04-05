from init import *
import logger

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