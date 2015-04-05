import re
import requests
from PyQt4.QtGui import QIcon

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
MIN_PP_RANK = 10000

ERROR_LOG = open('error_log.txt', 'w')

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