from __future__ import print_function
import sys
from init import *


def log_data(beatmaps):
    error_msg("log_data: Started logging.", None)
    json_file, source_file, creator_file, profile_file, user_page_file = open_log_files()

    for beatmap in beatmaps:
        if json_file is not None:
            try:
                json_file.write(beatmap.json + '\n')
            except Exception as err:
                error_msg('log_data: Could not write to json_file.', err)
        if source_file is not None:
            try:
                source_file.write(beatmap.source + '\n')
            except Exception as err:
                error_msg('log_data: Could not write to source_file.', err)
        if creator_file is not None:
            try:
                creator_file.write(beatmap.creator + '\n')
            except Exception as err:
                error_msg('log_data: Could not write to creator_file.', err)
        if profile_file is not None:
            try:
                profile_file.write(beatmap.profile + '\n')
            except Exception as err:
                error_msg('log_data: Could not write to profile_file.', err)
                # TODO
                # REMOVE COMMENTS AFTER USER PAGE SCRAPING FIXED
                # if user_page_file is not None:
                # try:
                #        user_page_file.write(beatmap.user_page + '\n')
                #    except Exception as err:
                #        error_msg('log_data: Could not write to user_page_file.', err)

    close_log_files(json_file, source_file, creator_file, profile_file, user_page_file)
    error_msg("log_data: Finished logging.", None)


def open_log_files():
    error_msg("open_log_files: Opening files.", None)
    try:
        json_file = open('json.txt', 'w')
    except Exception as err:
        error_msg('open_log_files: Could not open json_file.', err)
        json_file = None
    try:
        source_file = open('source.txt', 'w')
    except Exception as err:
        error_msg('open_log_files: Could not open source_file.', err)
        source_file = None
    try:
        creator_file = open('creator.txt', 'w')
    except Exception as err:
        error_msg('open_log_files: Could not open creator_file.', err)
        creator_file = None
    try:
        profile_file = open('profile.txt', 'w')
    except Exception as err:
        error_msg('open_log_files: Could not open profile_file.', err)
        profile_file = None
    try:
        user_page_file = open('user_page.txt', 'w')
    except Exception as err:
        error_msg('open_log_files: Could not open user_page file.', err)
        user_page_file = None

    return json_file, source_file, creator_file, profile_file, user_page_file


def close_log_files(json_file, source_file, creator_file, profile_file, user_page_file):
    error_msg("close_log_files: Closing files.", None)
    try:
        json_file.close()
    except Exception as err:
        error_msg('close_log_files: Could not close json_file.', err)
    try:
        source_file.close()
    except Exception as err:
        error_msg('close_log_files: Could not close source_file.', err)
    try:
        creator_file.close()
    except Exception as err:
        error_msg('close_log_files: Could not close creator_file.', err)
    try:
        profile_file.close()
    except Exception as err:
        error_msg('close_log_files: Could not close profile_file.', err)
    try:
        user_page_file.close()
    except Exception as err:
        error_msg('close_log_files: Could not close user_page_file.', err)


def error_msg(msg, err):
    print(msg, file=sys.stderr)
    try:
        ERROR_LOG.write(msg + '\n' + str(err) + '\n\n')
    except Exception as e:
        print('CANNOT WRITE INTO ERROR LOG.', file=sys.stderr)
        print(str(e))