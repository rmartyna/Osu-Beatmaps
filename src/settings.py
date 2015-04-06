import pickle
import logger
import shutil
import os
from init import *


def load_settings():
    logger.error_msg("load_settings: Started loading settings.", None)

    if not (os.path.exists(SETTINGS['DOWNLOAD_FOLDER']) and os.path.isdir(SETTINGS['DOWNLOAD_FOLDER'])):
        os.makedirs(SETTINGS['DOWNLOAD_FOLDER'])
    if not (os.path.exists('temp') and os.path.isdir('temp')):
        os.makedirs('temp')

    try:
        settings = pickle.load(open("config.dat", "rb"))
        logger.error_msg("load_settings: Found config file.", None)
    except IOError:
        settings = dict()
        logger.error_msg("load_settings: Could not find config file", None)

    try:
        SETTINGS['USERNAME'] = settings["USERNAME"]
        logger.error_msg("load_settings: Loaded username.", None)
    except KeyError:
        logger.error_msg("load_settings: Could not load username.", None)
        pass
    try:
        SETTINGS['PASSWORD'] = settings["PASSWORD"]
        logger.error_msg("load_settings: Loaded password.", None)
    except KeyError:
        logger.error_msg("load_settings: Could not load password.", None)
        pass
    try:
        SETTINGS['DOWNLOAD_FOLDER'] = settings["DOWNLOAD_FOLDER"]
        logger.error_msg("load_settings: Loaded download folder.", None)
    except KeyError:
        logger.error_msg("load_settings: Could not load download folder.", None)
        pass


def save_settings():
    shutil.rmtree('temp')

    try:
        print(SETTINGS['USERNAME'])
        print(SETTINGS['PASSWORD'])
        print(SETTINGS['DOWNLOAD_FOLDER'])
        pickle.dump(SETTINGS, open("config.dat", "wb"))
        logger.error_msg("save_settings: Saved settings.", None)
    except Exception as err:
        logger.error_msg("save_settings: Could not save settings.", err)