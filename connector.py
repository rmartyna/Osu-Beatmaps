import requests
from init import *

SESSION = None

def connect():
    global SESSION


def login():
    SESSION.post('https://osu.ppy.sh/forum/ucp.php?mode=login', data=LOGIN_DATA)