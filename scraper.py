import requests
import pickle
import re
import os

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
INVALID_CHARACTERS_ = re.compile(r'[\\/\?:\*<>|"]')

LAST_PAGE = 1

DOWNLOAD_FOLDER = r'C:\Users\user\Desktop\beatmaps'


class Beatmap:
    def __init__(self, id_):
        self.id_ = id_
        self.source = None
        self.json = None


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
    except IOError:
        pass

    for beatmap in beatmaps:
        if beatmap.id_ not in database:
            if favourited_times(beatmap) > 2 and star_difficulty(beatmap) > 4:
                database.add(beatmap.id_)
                download_beatmap(session, beatmap)

    pickle.dump(database, open("database.dat", "wb"))


def log_data(beatmaps):
    json_file = open('json.txt', 'w')
    source_file = open('source.txt', 'w')
    for beatmap in beatmaps:
        json_file.write(beatmap.json + '\n')
        source_file.write(beatmap.source + '\n')

    json_file.close()
    source_file.close()


def scrape_data(session, beatmaps):
    scrape_beatmaps_id(session, beatmaps)
    scrape_beatmaps_source(session, beatmaps)
    scrape_beatmaps_json(session, beatmaps)


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
    return INVALID_CHARACTERS_.sub('', artist + ' - ' + title)


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