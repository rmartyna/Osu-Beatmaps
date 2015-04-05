import pickle
import logger
from init import *


def load_settings(self):
    global USERNAME, PASSWORD, DOWNLOAD_FOLDER, SETTINGS
    try:
        SETTINGS = pickle.load(open("config.dat", "rb"))
    except IOError:
        SETTINGS = dict()

    try:
        USERNAME = SETTINGS["username"]
    except KeyError:
        pass
    try:
        PASSWORD = SETTINGS["password"]
    except KeyError:
        pass
    try:
        DOWNLOAD_FOLDER = SETTINGS["download_folder"]
    except KeyError:
        pass


def save_settings(self):
    try:
        pickle.dump(SETTINGS, open("config.dat", "wb"))
        logger.error_msg("Saved settings.", None)
    except Exception as err:
        logger.error_msg("save_settings: Could not save settings.", err)
