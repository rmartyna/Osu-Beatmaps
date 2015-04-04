import re

LOGIN_DATA = None

FAVOURITED_TIMES_ = None
BEATMAP_ID_ = None
STAR_DIFFICULTY_ = None
GAME_MODE_ = None
ARTIST_ = None
TITLE_ = None
USER_ID_ = None
RANKED_ = None
PENDING_ = None
GRAVEYARDED_ = None
PP_RANK_ = None
CREATOR_ = None
INVALID_CHARACTERS_ = None

FIRST_PAGE = None
LAST_PAGE = None

MIN_FAVOURITED = None
MIN_DIFFICULTY = None
MIN_RANKED = None
MIN_NON_RANKED = None
MIN_PP_RANK = None

DOWNLOAD_FOLDER = None
ERROR_LOG = None

VERSION = None
DATE = None
EMAIL = None
GITHUB = None

USERNAME = None
PASSWORD = None
LOGGED = None

SESSION = None

def init():
    global LOGIN_DATA, FAVOURITED_TIMES_, BEATMAP_ID_, STAR_DIFFICULTY_, GAME_MODE_, \
        ARTIST_, TITLE_, USER_ID_, RANKED_, PENDING_, GRAVEYARDED_, PP_RANK_, CREATOR_, \
        INVALID_CHARACTERS_, FIRST_PAGE, LAST_PAGE, MIN_FAVOURITED, MIN_DIFFICULTY, \
        MIN_RANKED, MIN_NON_RANKED, MIN_PP_RANK, DOWNLOAD_FOLDER, ERROR_LOG, \
        VERSION, DATE, EMAIL, GITHUB, USERNAME, PASSWORD, LOGGED, SESSION

    LOGIN_DATA = {
        'username': None,
        'password': None,
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
    LAST_PAGE = 125

    MIN_FAVOURITED = 5
    MIN_DIFFICULTY = 4.0
    MIN_RANKED = 1
    MIN_NON_RANKED = 5
    MIN_PP_RANK = 10000

    DOWNLOAD_FOLDER = r'E:\beatmaps'
    ERROR_LOG = open('error_log.txt', 'w')

    VERSION = "0.1"
    DATE = "4th April 2015"
    EMAIL = "rmartyna94@gmail.com"
    GITHUB = r"https://github.com/rmartyna/Osu-Beatmaps/"

    USERNAME = None
    PASSWORD = None
    LOGGED = False

    SESSION = requests.Session()