import pickle
import os
from init import *
import logger
import evaluator


def download_good_maps(session, beatmaps):
    try:
        database = pickle.load(open("database.dat", "rb"))
    except IOError:
        database = set()

    if not (os.path.exists(SETTINGS['DOWNLOAD_FOLDER']) and os.path.isdir(SETTINGS['DOWNLOAD_FOLDER'])):
        try:
            os.makedirs(SETTINGS['DOWNLOAD_FOLDER'])
        except WindowsError as err:
            logger.error_msg('download_good_maps: Could not make download directory.', err)
            return
    try:
        for index, beatmap in enumerate(beatmaps):
            print('download_good_maps ' + str(index + 1) + '/' + str(len(beatmaps)))
            if beatmap.id_ not in database:
                if evaluator.ok_difficulty(beatmap) and (evaluator.ok_creator(beatmap)
                                                         or evaluator.ok_favourited(beatmap)):
                    try:
                        database.add(beatmap.id_)
                        try:
                            download_beatmap(session, beatmap)
                        except Exception as err:
                            logger.error_msg('download_good_maps: Could not download beatmap ' + beatmap.id_ + '.', err)
                            continue
                    except Exception as err:
                        logger.error_msg('download_good_maps: Could not add id ' + beatmap.id_ + ' to database.', err)
                        continue
    finally:
        try:
            pickle.dump(database, open("database.dat", "wb"))
        except Exception as err:
            logger.error_msg('download_good_maps: Could not dump database.', err)


def download_beatmap(session, beatmap):
    try:
        absolute_path = os.path.join(os.path.join(SETTINGS['DOWNLOAD_FOLDER'],
                                                  evaluator.beatmap_name(beatmap) + '.osz'))
    except Exception as err:
        logger.error_msg('download_beatmap: Could not make absolute path.', err)
        return
    beatmap_file = None
    try:
        beatmap_file = open(absolute_path, 'wb')
        try:
            beatmap_data = session.get('https://osu.ppy.sh/d/' + beatmap.id_)
            try:
                beatmap_file.write(beatmap_data.content)
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