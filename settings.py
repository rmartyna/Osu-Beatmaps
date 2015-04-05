import pickle
import logger
from init import *


def load_settings(self):
    global USERNAME, PASSWORD, DOWNLOAD_FOLDER, SETTINGS
    logger.error_msg("load_settings: Started loading settings.", None)
    try:
        SETTINGS = pickle.load(open("config.dat", "rb"))
        logger.error_msg("load_settings: Found config file.", None)
    except IOError:
        SETTINGS = dict()
        logger.error_msg("load_settings: Could not find config file", None)

    try:
        USERNAME = SETTINGS["username"]
        logger.error_msg("load_settings: Loaded username.", None)
    except KeyError:
        logger.error_msg("load_settings: Could not load username.", None)
        pass
    try:
        PASSWORD = SETTINGS["password"]
        logger.error_msg("load_settings: Loaded password.", None)
    except KeyError:
        logger.error_msg("load_settings: Could not load password.", None)
        pass
    try:
        DOWNLOAD_FOLDER = SETTINGS["download_folder"]
        logger.error_msg("load_settings: Loaded download folder.", None)
    except KeyError:
        logger.error_msg("load_settings: Could not load download folder.", None)
        pass


def save_settings(self):
    try:
        pickle.dump(SETTINGS, open("config.dat", "wb"))
        logger.error_msg("save_settings: Saved settings.", None)
    except Exception as err:
        logger.error_msg("save_settings: Could not save settings.", err)
