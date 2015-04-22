import shutil
import os
from init import *
import logger


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
    except KeyError:
        pass
    try:
        SETTINGS['PASSWORD'] = settings["PASSWORD"]
    except KeyError:
        pass
    try:
        SETTINGS['DOWNLOAD_FOLDER'] = settings["DOWNLOAD_FOLDER"]
    except KeyError:
        pass
    try:
        SETTINGS['MIN_FAVOURITED'] = settings['MIN_FAVOURITED']
    except KeyError:
        pass
    try:
        SETTINGS['MIN_DIFFICULTY'] = settings['MIN_DIFFICULTY']
    except KeyError:
        pass
    try:
        SETTINGS['MIN_RANKED'] = settings['MIN_RANKED']
    except KeyError:
        pass
    try:
        SETTINGS['MIN_NON_RANKED'] = settings['MIN_NON_RANKED']
    except KeyError:
        pass
    try:
        SETTINGS['MIN_PP_RANK'] = settings['MIN_PP_RANK']
    except KeyError:
        pass


def save_settings():
    logger.error_msg("save_settings: Started saving settings.", None)
    try:
        shutil.rmtree('temp')
    except WindowsError:
        logger.error_msg("save_settings: Could not find temp folder.", None)

    try:
        pickle.dump(SETTINGS, open("config.dat", "wb"))
        logger.error_msg("save_settings: Saved settings.", None)
    except Exception as err:
        logger.error_msg("save_settings: Could not save settings.", err)
