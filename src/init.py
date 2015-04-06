import re
import requests
import pickle


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
LOGIN_PAGE_ = re.compile(r'Welcome, <b><a href=\"/u/([0-9]+)\">')
IMAGE_URL_ = re.compile(r'<img class=\'bmt\' src=\"([^\"]+)\">')

FIRST_PAGE = 1
LAST_PAGE = 125

MIN_FAVOURITED = 5
MIN_DIFFICULTY = 4.0
MIN_RANKED = 1
MIN_NON_RANKED = 5
MIN_PP_RANK = 5000

ERROR_LOG = open('../error_log.txt', 'w')

VERSION = "0.1"
DATE = "4th April 2015"
EMAIL = "rmartyna94@gmail.com"
GITHUB = r"https://github.com/rmartyna/Osu-Beatmaps/"

SETTINGS = {
    'USERNAME': None,
    'PASSWORD': None,
    'DOWNLOAD_FOLDER': r'D:\beatmaps'}

SESSION = requests.Session()

LOGIN_URL = 'https://osu.ppy.sh/forum/ucp.php?mode=login'
MAIN_PAGE_URL = 'https://osu.ppy.sh'
ALL_MAPS_URL = 'https://osu.ppy.sh/p/beatmaplist?l=1&r=4&q=&g=0&la=0&s=4&o=1&m=-1&page='
MAP_PAGE_URL = 'https://osu.ppy.sh/s/'
MAP_JSON_URL = 'https://osu.ppy.sh/api/get_beatmaps?k=c5878839513d6eb99dbf09f8244653332b93eb3c&s='
MAP_CREATOR_URL = 'https://osu.ppy.sh/api/get_user?k=c5878839513d6eb99dbf09f8244653332b93eb3c&u='
MAP_PROFILE_URL_START = 'https://osu.ppy.sh/pages/include/profile-beatmaps.php?u='
MAP_PROFILE_URL_END = '&m=0'
MAP_IMAGE_URL_START = 'https://b.ppy.sh/thumb/'
MAP_IMAGE_URL_END = 'l.jpg'
MAP_SONG_URL_START = 'http://b.ppy.sh/preview/'
MAP_SONG_URL_END = '.mp3'

CURRENTLY_PLAYING = {'p': None,
                     'id': None,
                     't': None}


try:
    DATABASE = pickle.load(open("../database.dat", "rb"))
except IOError:
    DATABASE = set()