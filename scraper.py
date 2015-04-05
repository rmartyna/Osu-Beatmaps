from __future__ import print_function
import logger
from init import *
import Beatmap


# TODO
# MOST IMPORTANTLY: ADD TESTS
# ADD ADDITIONAL FUNCTIONALITY
# ADD GUI
# LEARN HOW TO SCRAPE TOTAL KUDOSU EARNED(FAKE JAVASCRIPT)
def scrape_data(beatmaps, page):
    logger.error_msg("scrape_data: Start scraping.", None)
    scrape_beatmaps_id(beatmaps, page)
    logger.error_msg("scrape_data: Finished scraping ids.", None)
    scrape_beatmaps_source(beatmaps)
    logger.error_msg("scrape_data: Finished scraping source.", None)
    scrape_beatmaps_json(beatmaps)
    logger.error_msg("scrape_data: Finished scraping json.", None)
    scrape_beatmaps_creator(beatmaps)
    logger.error_msg("scrape_data: Finished scraping creator.", None)
    scrape_beatmaps_profile(beatmaps)
    logger.error_msg("scrape_data: Finished scraping profile.", None)
    scrape_beatmaps_user_page(beatmaps)
    logger.error_msg("scrape_data: Finished scraping user_page", None)
    logger.error_msg("scrape_data: Finished scraping.", None)


def scrape_beatmaps_id(beatmaps, page):
    try:
        response = SESSION.get('https://osu.ppy.sh/p/beatmaplist?l=1&r=4&q=&g=0&la=0&s=4&o=1&m=-1&page='
                               + str(page))
        try:
            result = BEATMAP_ID_.findall(response.content)
            for beatmap_id in result:
                beatmaps.append(Beatmap.Beatmap(beatmap_id))
        except Exception as err:
            logger.error_msg('scrape_beatmaps_id: Error finding ids on page.', err)
    except requests.RequestException as err:
        logger.error_msg('scrape_beatmaps_id: Error getting page ' + str(page) + '.', err)


def scrape_beatmaps_source(beatmaps):
    to_remove = []
    for index, beatmap in enumerate(beatmaps):
        try:
            response = SESSION.get('https://osu.ppy.sh/s/'
                                   + beatmap.id_)
            beatmap.source = response.content
        except requests.RequestException as err:
            logger.error_msg('scrape_beatmaps_source: Error getting source page on beatmap '
                             + str(beatmap.id_) + '.', err)
            to_remove.append(index)
    remove_beatmaps(beatmaps, to_remove)


def scrape_beatmaps_json(beatmaps):
    to_remove = []
    for index, beatmap in enumerate(beatmaps):
        try:
            response = SESSION.get('https://osu.ppy.sh/api/get_beatmaps?k=c5878839513d6eb99dbf09f8244653332b93eb3c&s='
                                   + beatmap.id_)
            beatmap.json = response.content
        except requests.RequestException as err:
            logger.error_msg('scrape_beatmaps_json: Error getting json on beatmap '
                             + str(beatmap.id_) + '.', err)
            to_remove.append(index)
    remove_beatmaps(beatmaps, to_remove)


def scrape_beatmaps_creator(beatmaps):
    to_remove = []
    for index, beatmap in enumerate(beatmaps):
        try:
            creator = CREATOR_.search(beatmap.json).group(1)
            try:
                response = SESSION.get('https://osu.ppy.sh/api/get_user?k=c5878839513d6eb99dbf09f8244653332b93eb3c&u='
                                       + creator)
                beatmap.creator = response.content
            except requests.RequestException as err:
                logger.error_msg('scrape_beatmaps_creator: Could not get creator page of baetmap '
                                 + beatmap.id_ + '.', err)
                to_remove.append(index)
        except Exception as err:
            logger.error_msg('scrape_beatmaps_creator: Error finding creator of beatmap '
                             + beatmap.id_ + '.', err)
            to_remove.append(index)
    remove_beatmaps(beatmaps, to_remove)


def scrape_beatmaps_profile(beatmaps):
    to_remove = []
    for index, beatmap in enumerate(beatmaps):
        try:
            user_id = USER_ID_.search(beatmap.creator).group(1)
            try:
                response = SESSION.get('https://osu.ppy.sh/pages/include/profile-beatmaps.php?u='
                                       + user_id + '&m=0')
                beatmap.profile = response.content
            except requests.RequestException as err:
                logger.error_msg('scrape_beatmaps_profile: Could not get profile page of creator '
                                 + str(user_id) + '.', err)
                to_remove.append(index)
        except Exception as err:
            logger.error_msg('scrape_beatmaps_profile: Error finding user_id of beatmap '
                             + beatmap.id_ + '.', err)
            to_remove.append(index)
    remove_beatmaps(beatmaps, to_remove)


# TODO
# ADD METHOD TO SCRAPE KUDOSU FOR USER PAGE
# NEED TO FAKE JAVASCRIPT
def scrape_beatmaps_user_page(beatmaps):
    pass


def remove_beatmaps(beatmaps, to_remove):
    for index in reversed(to_remove):
        try:
            beatmaps.pop(index)
        except Exception as err:
            logger.error_msg('remove_beatmaps: Error while popping from beatmaps list.', err)