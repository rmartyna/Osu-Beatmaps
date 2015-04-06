import os
from init import *
import logger
import evaluator


def download_good_maps(beatmaps):
    if not (os.path.exists(SETTINGS['DOWNLOAD_FOLDER']) and os.path.isdir(SETTINGS['DOWNLOAD_FOLDER'])):
        try:
            os.makedirs(SETTINGS['DOWNLOAD_FOLDER'])
        except WindowsError as err:
            logger.error_msg('download_good_maps: Could not make download directory.', err)
            return
    try:
        for index, beatmap in enumerate(beatmaps):
            if beatmap.id_ not in DATABASE:
                if evaluator.ok_difficulty(beatmap) and (evaluator.ok_creator(beatmap)
                                                         or evaluator.ok_favourited(beatmap)):
                    try:
                        DATABASE.add(beatmap.id_)
                        try:
                            download_beatmap(beatmap)
                        except Exception as err:
                            logger.error_msg('download_good_maps: Could not download beatmap ' + beatmap.id_ + '.', err)
                            continue
                    except Exception as err:
                        logger.error_msg('download_good_maps: Could not add id ' + beatmap.id_ + ' to database.', err)
                        continue
    finally:
        try:
            pickle.dump(DATABASE, open("database.dat", "wb"))
        except Exception as err:
            logger.error_msg('download_good_maps: Could not dump database.', err)


def download_beatmap(beatmap):
    logger.error_msg("download_beatmap: Downloading beatmap: " + beatmap.id_ + ".", None)
    try:
        absolute_path = os.path.join(os.path.join(SETTINGS['DOWNLOAD_FOLDER'],
                                                  beatmap.get_name() + '.osz'))
    except Exception as err:
        logger.error_msg('download_beatmap: Could not make absolute path.', err)
        return
    beatmap_file = None
    try:
        beatmap_file = open(absolute_path, 'wb')
        try:
            beatmap_data = SESSION.get('https://osu.ppy.sh/d/' + beatmap.id_)
            try:
                beatmap_file.write(beatmap_data.content)
                logger.error_msg("download_beatmap: Finished downloading beatmap: " + beatmap.id_ + ".", None)
                try:
                    DATABASE.add(beatmap.id_)
                    pickle.dump(DATABASE, open("database.dat", "wb"))
                except Exception as err:
                    logger.error_msg('download_beatmap: Could not dump database.', err)
            except Exception as err:
                logger.error_msg('download_beatmap: Could not write beatmap ' + beatmap.id_ + ' into file.', err)
        except requests.RequestException as err:
            logger.error_msg('download_beatmap: Could not download beatmap '
                             + beatmap.id_ + ".", err)
    except Exception as err:
        logger.error_msg('download_beatmap: Could not open file.', err)
    finally:
        try:
            beatmap_file.close()
        except Exception as err:
            logger.error_msg('download_beatmap: Could not close file.', err)