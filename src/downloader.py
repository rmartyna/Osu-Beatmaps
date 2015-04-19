import os
from init import *
import logger


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
            beatmap_data = SESSION[0].get('https://osu.ppy.sh/d/' + beatmap.id_)
            try:
                beatmap_file.write(beatmap_data.content)
                logger.error_msg("download_beatmap: Finished downloading beatmap: " + beatmap.id_ + ".", None)
                beatmap.add_to_database()
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