from __future__ import print_function
import threading
from init import *
import logger
import Beatmap


def scrape_data(beatmaps, page):
    logger.error_msg("scrape_data: Start scraping.", None)

    scrape_beatmaps_id(beatmaps, page)
    scrape_beatmaps_json(beatmaps)
    scrape_beatmaps_creator(beatmaps)
    scrape_beatmaps_profile(beatmaps)
    scrape_beatmaps_user_page(beatmaps)


def scrape_data_after_filtering(beatmaps):
    logger.error_msg("scrape_data_after_filtering: Start scraping.", None)

    scrape_beatmaps_images(beatmaps)
    scrape_beatmaps_songs(beatmaps)


def scrape_beatmaps_id(beatmaps, page):
    try:
        response = SESSION[0].get(ALL_MAPS_URL + str(page))
        try:
            result = BEATMAP_ID_.findall(response.content)
            for index, beatmap_id in enumerate(result):
                beatmaps.append(Beatmap.Beatmap(beatmap_id, response.content, index))
        except Exception as err:
            logger.error_msg('scrape_beatmaps_id: Error finding ids on page ' + str(page) + '.', err)
    except requests.RequestException as err:
        logger.error_msg('scrape_beatmaps_id: Error getting page ' + str(page) + '.', err)


def scrape_beatmaps_json(beatmaps):
    scrape_mutltiple_pages(beatmaps, scrape_json)


def scrape_json(beatmap, to_remove, index):
    try:
        response = SESSION[0].get(MAP_JSON_URL + beatmap.id_)
        beatmap.json = response.content
    except requests.RequestException as err:
        logger.error_msg('scrape_json: Error getting json on beatmap '
                         + str(beatmap.id_) + '.', err)
        to_remove.append(index)


def scrape_beatmaps_creator(beatmaps):
    scrape_mutltiple_pages(beatmaps, scrape_creator)


def scrape_creator(beatmap, to_remove, index):
    try:
        creator = CREATOR_.search(beatmap.json).group(1)
        try:
            response = SESSION[0].get(MAP_CREATOR_URL + creator)
            beatmap.creator = response.content
        except requests.RequestException as err:
            logger.error_msg('scrape_reator: Could not get creator page of beatmap '
                             + beatmap.id_ + '.', err)
            to_remove.append(index)
    except Exception as err:
        logger.error_msg('scrape_creator: Error finding creator of beatmap '
                         + beatmap.id_ + '.', err)
        to_remove.append(index)


def scrape_beatmaps_profile(beatmaps):
    scrape_mutltiple_pages(beatmaps, scrape_profile)


def scrape_profile(beatmap, to_remove, index):
    try:
        user_id = USER_ID_.search(beatmap.creator).group(1)
        try:
            response = SESSION[0].get(MAP_PROFILE_URL_START + user_id + MAP_PROFILE_URL_END)
            beatmap.profile = response.content
        except requests.RequestException as err:
            logger.error_msg('scrape_profile: Could not get profile page of creator '
                             + user_id + '.', err)
            to_remove.append(index)
    except Exception as err:
        logger.error_msg('scrape_profile: Error finding user_id of beatmap '
                         + beatmap.id_ + '.', err)
        to_remove.append(index)


def scrape_beatmaps_user_page(beatmaps):
    pass


def scrape_beatmaps_images(beatmaps):
    scrape_mutliple_pages_without_deleting(beatmaps, scrape_image)


def scrape_image(beatmap):
    try:
        image = SESSION[0].get(MAP_IMAGE_URL_START + beatmap.id_ + MAP_IMAGE_URL_END)
        if len(image.content) > 0:
            try:
                f = open("temp/" + beatmap.id_ + '.jpg', 'wb')
                try:
                    f.write(image.content)
                    try:
                        f.close()
                    except Exception as err:
                        logger.error_msg('scrape_image: Could not close file of beatmap '
                                         + beatmap.id_ + '.', err)
                except Exception as err:
                    logger.error_msg('scrape_image: Could not write image of beatmap '
                                     + beatmap.id_ + ' to file.', err)
            except Exception as err:
                logger.error_msg('scrape__image: Could not open file for image of beatmap '
                                 + beatmap.id_ + '.', err)
    except requests.ConnectionError as err:
        logger.error_msg('scrape_image: Could not download image of beatmap '
                         + beatmap.id_ + '.', err)


def scrape_beatmaps_songs(beatmaps):
    scrape_mutliple_pages_without_deleting(beatmaps, scrape_song)


def scrape_song(beatmap):
    try:
        response = SESSION[0].get(MAP_SONG_URL_START + beatmap.id_ + MAP_SONG_URL_END)
        try:
            f = open('temp/' + beatmap.id_ + '.mp3', 'wb')
            try:
                f.write(response.content)
                try:
                    f.close()
                except Exception as err:
                    logger.error_msg("scrape_song: Could not close file of beatmap "
                                     + beatmap.id_ + '.', err)
            except Exception as err:
                logger.error_msg('scrape_song: Could not write song of beatmap '
                                 + beatmap.id_ + ' to file.', err)
        except Exception as err:
            logger.error_msg('scrape_song: Could not open file for song of beatmap '
                             + beatmap.id_ + '.', err)
    except Exception as err:
        logger.error_msg('scrape_song: Could not download song of beatmap '
                         + beatmap.id_ + '.', err)


def remove_beatmaps(beatmaps, to_remove):
    for index in reversed(to_remove):
        try:
            beatmaps.pop(index)
        except Exception as err:
            logger.error_msg('remove_beatmaps: Error while popping from beatmaps list.', err)


def scrape_mutltiple_pages(beatmaps, target):
    to_remove = []
    threads = []
    for index, beatmap in enumerate(beatmaps):
        thread = threading.Thread(target=target, args=(beatmap, to_remove, index))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    remove_beatmaps(beatmaps, to_remove)


def scrape_mutliple_pages_without_deleting(beatmaps, target):
    threads = []
    for beatmap in beatmaps:
        thread = threading.Thread(target=target, args=(beatmap,))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()