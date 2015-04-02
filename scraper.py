import requests
import pickle
import re
import os

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

LAST_PAGE = 1
MIN_FAVOURITED = 3
MIN_DIFFICULTY = 4.0
MIN_RANKED = 1
MIN_NON_RANKED = 3
MIN_PP_RANK = 10000

DOWNLOAD_FOLDER = r'C:\Users\user\Desktop\beatmaps'


class Beatmap:
    def __init__(self, id_):
        self.id_ = id_
        self.source = None
        self.json = None
        self.creator = None
        self.profile = None
        self.user_page = None


def main():
    session = requests.Session()
    beatmaps = []
    login(session)
    scrape_data(session, beatmaps)
    log_data(beatmaps)
    # for beatmap in beatmaps:
    #    print(str(beatmap.id_) + "    " + str(favourited_times(beatmap)) + "    " + str(star_difficulty(beatmap)))
    download_good_maps(session, beatmaps)
    session.close()


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
        user_id = USER_ID_.search(beatmap.creator).group(1)
        response = session.get('https://osu.ppy.sh/pages/include/profile-beatmaps.php?u='
                               + user_id + '&m=0')
        beatmap.profile = response.content


def scrape_beatmaps_id(session, beatmaps):

    for page in range(1, LAST_PAGE + 1):
        response = session.get('https://osu.ppy.sh/p/beatmaplist?l=1&r=4&q=&g=0&la=0&s=4&o=1&m=-1&page='
                               + str(page))
        result = BEATMAP_ID_.findall(response.content)
        for beatmap_id in result:
            beatmaps.append(Beatmap(beatmap_id))


def scrape_beatmaps_source(session, beatmaps):
    for beatmap in beatmaps:
        response = session.get('https://osu.ppy.sh/s/'
                               + beatmap.id_)
        beatmap.source = response.content


def scrape_beatmaps_json(session, beatmaps):
    for beatmap in beatmaps:
        response = session.get('https://osu.ppy.sh/api/get_beatmaps?k=c5878839513d6eb99dbf09f8244653332b93eb3c&s='
                               + beatmap.id_)
        beatmap.json = response.content


def login(session):
    session.post('https://osu.ppy.sh/forum/ucp.php?mode=login', data=LOGIN_DATA)


def download_beatmap(session, beatmap):
    beatmap_file = open(os.path.join(DOWNLOAD_FOLDER, beatmap_name(beatmap) + '.osz'), 'wb')
    beatmap_data = session.get('https://osu.ppy.sh/d/' + beatmap.id_)
    beatmap_file.write(beatmap_data.content)
    beatmap_file.close()


def beatmap_name(beatmap):
    artist = ARTIST_.search(beatmap.json).group(1)
    title = TITLE_.search(beatmap.json).group(1)
    return INVALID_CHARACTERS_.sub('', str(beatmap.id) + ' ' + artist + ' - ' + title)


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


if __name__ == "__main__":
    main()