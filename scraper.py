from __future__ import print_function
import requests
from requests.exceptions import RequestException
import pickle
import re
import os
import sys


# TODO
# MOST IMPORTANTLY: ADD TESTS
# ADD ADDITIONAL FUNCTIONALITY
# ADD GUI
# LEARN HOW TO SCRAPE TOTAL KUDOSU EARNED(FAKE JAVASCRIPT)


LOGIN_DATA = {
    'username': 'krur',
    'password': 'zlototopotega',
    'login': 'Login'
}
FAVOURITED_TIMES_ = re.compile(r'<div><b>Favourited ([0-9]+) times?</b> in total')
BEATMAP_ID_ = re.compile(r'a href=\'/s/([0-9]+)\'')
STAR_DIFFICULTY_ = re.compile(r'\"difficultyrating\":\"([0-9\.]+)\"')
GAME_MODE_ = re.compile(r'\"mode\":\"([0123])\"')
ARTIST_ = re.compile(r'\"artist\":\"([^\"]+)\"')
TITLE_ = re.compile(r'\"title\":\"([^\"]+)\"')
USER_ID_ = re.compile(r'\"user_id\":\"([0-9]+)\"')
RANKED_ = re.compile(r'Ranked & Approved Beatmaps \(([0-9]+)\)')
PENDING_ = re.compile(r'Pending Beatmaps \([0-9]+\)')
GRAVEYARDED_ = re.compile(r'Graveyarded Beatmaps \([0-9]+\)')
PP_RANK_ = re.compile(r'\"pp_rank\":\"([0-9]+)\"')
CREATOR_ = re.compile(r'\"creator\":\"([^\"]+)\"')
INVALID_CHARACTERS_ = re.compile(r'[\\/\?:\*<>|"]')

FIRST_PAGE = 1
LAST_PAGE = 1

MIN_FAVOURITED = 5
MIN_DIFFICULTY = 4.0
MIN_RANKED = 1
MIN_NON_RANKED = 5
MIN_PP_RANK = 10000

DOWNLOAD_FOLDER = r'C:\Users\user\Desktop\beatmaps'
ERROR_LOG = open('error_log.txt', 'w')


class Beatmap:
    def __init__(self, id_):
        self.id_ = id_
        self.source = None
        self.json = None
        self.creator = None
        self.profile = None
        self.user_page = None


def main():
    session = None
    try:
        session = requests.Session()
        beatmaps = []
        try:
            login(session)
        except RequestException as err:
            error_msg('Main: Could not login into Osu!', err)
            return
        try:
            scrape_data(session, beatmaps)
        except RequestException as err:
            error_msg('Main: Could not scrape data properly.', err)
            return
        try:
            log_data(beatmaps)
        except Exception as err:
            error_msg('Main: Could not log data.', err)
        try:
            download_good_maps(session, beatmaps)
        except Exception as err:
            error_msg('Main: Error while downloading maps.', err)
            return
    except RequestException as err:
        error_msg('Main: Could not open session.', err)
        return
    finally:
        try:
            session.close()
        except RequestException as err:
            error_msg('Main: Could not close session.', err)
            return


def download_good_maps(session, beatmaps):
    try:
        database = pickle.load(open("database.dat", "rb"))
    except IOError:
        database = set()

    try:
        os.makedirs(DOWNLOAD_FOLDER)
    except WindowsError:
        pass

    for beatmap in beatmaps:
        if beatmap.id_ not in database:
            if ok_difficulty(beatmap) and (ok_creator(beatmap) or ok_favourited(beatmap)):
                database.add(beatmap.id_)
                download_beatmap(session, beatmap)

    pickle.dump(database, open("database.dat", "wb"))


def ok_favourited(beatmap):
    return favourited_times(beatmap) >= MIN_FAVOURITED


def ok_difficulty(beatmap):
    return star_difficulty(beatmap) >= MIN_DIFFICULTY


def ok_creator(beatmap):
    return ok_pp_rank(beatmap) or ok_kudosu(beatmap) or ok_maps(beatmap)


def ok_pp_rank(beatmap):
    pp_rank = PP_RANK_.search(beatmap.creator).group(1)
    return int(pp_rank) < MIN_PP_RANK


def ok_maps(beatmap):
    return ok_ranked(beatmap) or ok_non_ranked(beatmap)

# TODO
# FIRST FINISH SCRAPE_BEATMAPS_USER_PAGE
def ok_kudosu(beatmap):
    return False


def ok_ranked(beatmap):
    try:
        ranked = RANKED_.search(beatmap.profile).group(1)
    except (AttributeError, IndexError):
        ranked = 0

    return int(ranked) >= MIN_RANKED


def ok_non_ranked(beatmap):
    try:
        pending = PENDING_.search(beatmap.profile).group(1)
    except (AttributeError, IndexError):
        pending = 0
    try:
        graveyarded = GRAVEYARDED_.search(beatmap.profile).group(1)
    except (AttributeError, IndexError):
        graveyarded = 0

    return int(pending) + int(graveyarded) >= MIN_NON_RANKED


def log_data(beatmaps):
    json_file = open('json.txt', 'w')
    source_file = open('source.txt', 'w')
    creator_file = open('creator.txt', 'w')
    profile_file = open('profile.txt', 'w')
    user_page_file = open('user_page.txt', 'w')
    for beatmap in beatmaps:
        json_file.write(beatmap.json + '\n')
        source_file.write(beatmap.source + '\n')
        creator_file.write(beatmap.creator + '\n')
        profile_file.write(beatmap.profile + '\n')
        user_page_file.write(beatmap.user_page + '\n')

    json_file.close()
    source_file.close()
    creator_file.close()
    profile_file.close()
    user_page_file.close()


def scrape_data(session, beatmaps):
    scrape_beatmaps_id(session, beatmaps)
    scrape_beatmaps_source(session, beatmaps)
    scrape_beatmaps_json(session, beatmaps)
    scrape_beatmaps_creator(session, beatmaps)
    scrape_beatmaps_profile(session, beatmaps)
    scrape_beatmaps_user_page(session, beatmaps)


# TODO
# ADD METHOD TO SCRAPE KUDOSU FOR USER PAGE
# NEED TO FAKE JAVASCRIPT
def scrape_beatmaps_user_page(session, beatmaps):
    for beatmap in beatmaps:
        beatmap.user_page = '\n'


def scrape_beatmaps_creator(session, beatmaps):
    for beatmap in beatmaps:
        creator = CREATOR_.search(beatmap.json).group(1)
        response = session.get('https://osu.ppy.sh/api/get_user?k=c5878839513d6eb99dbf09f8244653332b93eb3c&u='
                               + creator)
        beatmap.creator = response.content


def scrape_beatmaps_profile(session, beatmaps):
    for beatmap in beatmaps:
        try:
            user_id = USER_ID_.search(beatmap.creator).group(1)
            try:
                response = session.get('https://osu.ppy.sh/pages/include/profile-beatmaps.php?u='
                                       + user_id + '&m=0')
                beatmap.profile = response.content
            except RequestException as err:
                error_msg('scrape_beatmaps_profile: Could not get profile page of creator '
                          + str(user_id) + '.', err)
        except Exception as err:
            error_msg('scrape_beatmaps_profile: Error finding user_id of creator of beatmap '
                      + beatmap.id_ + '.', err)


def scrape_beatmaps_id(session, beatmaps):
    for page in range(FIRST_PAGE, LAST_PAGE + 1):
        try:
            response = session.get('https://osu.ppy.sh/p/beatmaplist?l=1&r=4&q=&g=0&la=0&s=4&o=1&m=-1&page='
                                   + str(page))
            try:
                result = BEATMAP_ID_.findall(response.content)
                for beatmap_id in result:
                    beatmaps.append(Beatmap(beatmap_id))
            except Exception as err:
                error_msg('scrape_beatmaps_id: Error finding ids on page.', err)
        except RequestException as err:
            error_msg('scrape_beatmaps_id: Error getting page ' + str(page) + '.', err)


def scrape_beatmaps_source(session, beatmaps):
    for beatmap in beatmaps:
        try:
            response = session.get('https://osu.ppy.sh/s/'
                                   + beatmap.id_)
            beatmap.source = response.content
        except RequestException as err:
            error_msg('scrape_beatmaps_source: Error getting source page on beatmap '
                      + str(beatmap.id_) + '.', err)


def scrape_beatmaps_json(session, beatmaps):
    for beatmap in beatmaps:
        try:
            response = session.get('https://osu.ppy.sh/api/get_beatmaps?k=c5878839513d6eb99dbf09f8244653332b93eb3c&s='
                                   + beatmap.id_)
            beatmap.json = response.content
        except RequestException as err:
            error_msg('scrape_beatmaps_json: Error getting json on beatmap '
                      + str(beatmap.id_) + '.', err)


def login(session):
    session.post('https://osu.ppy.sh/forum/ucp.php?mode=login', data=LOGIN_DATA)


def download_beatmap(session, beatmap):
    try:
        absolute_path = os.path.join(os.path.join(DOWNLOAD_FOLDER, beatmap_name(beatmap) + '.osz'))
    except Exception as err:
        error_msg('download_beatmap: Could not make absolute path.', err)
        return
    beatmap_file = None
    try:
        beatmap_file = open(absolute_path, 'wb')
        try:
            beatmap_data = session.get('https://osu.ppy.sh/d/' + beatmap.id_)
            try:
                beatmap_file.write(beatmap_data.content)
            except Exception as err:
                error_msg('download_beatmap: Could not write beatmap ' + beatmap.id_ + ' into file.', err)
        except RequestException as err:
            error_msg('download_beatmap: Could not download beatmap '
                      + beatmap.id_ + ".", err)
    except Exception as err:
        error_msg('download_beatmap: Could not open file.', err)
    finally:
        try:
            beatmap_file.close()
        except Exception as err:
            error_msg('download_beatmap: Could not close file.', err)


def beatmap_name(beatmap):
    artist = ARTIST_.search(beatmap.json).group(1)
    title = TITLE_.search(beatmap.json).group(1)
    return INVALID_CHARACTERS_.sub('', str(beatmap.id_) + ' ' + artist + ' - ' + title)


def favourited_times(beatmap):
    number = FAVOURITED_TIMES_.search(beatmap.source).group(1)
    return int(number)


def star_difficulty(beatmap):
    difficulties = STAR_DIFFICULTY_.findall(beatmap.json)
    game_modes = GAME_MODE_.findall(beatmap.json)
    difficulties = [float(dif) for dif in difficulties]
    game_modes = [int(mode) for mode in game_modes]
    max_difficulty = 0
    for difficulty, mode in zip(difficulties, game_modes):
        if mode == 0 and max_difficulty < difficulty:
            max_difficulty = difficulty
    return max_difficulty


def error_msg(msg, err):
    print(msg, file=sys.stderr)
    try:
        ERROR_LOG.write(msg + '\n' + str(err) + '\n\n')
    except Exception as e:
        print('CANNOT WRITE INTO ERROR LOG.', file=sys.stderr)
        print(str(e))


if __name__ == "__main__":
    try:
        main()
    finally:
        ERROR_LOG.close()