from init import *
import logger


def ok_difficulty(beatmap):
    return star_difficulty(beatmap) >= MIN_DIFFICULTY


def star_difficulty(beatmap):
    try:
        difficulties = STAR_DIFFICULTY_.findall(beatmap.json)
        try:
            difficulties = [float(dif) for dif in difficulties]
        except Exception as err:
            logger.error_msg('star_difficulty: Error converting difficulties to float.', err)
            return -1
    except Exception as err:
        logger.error_msg('star_difficulty: Error finding difficulties in json of beatmap '
                         + beatmap.id_ + '.', err)
        return -1
    try:
        game_modes = GAME_MODE_.findall(beatmap.json)
        try:
            game_modes = [int(mode) for mode in game_modes]
        except Exception as err:
            logger.error_msg('star_difficulty: Error converting game modes to int.', err)
            return -1
    except Exception as err:
        logger.error_msg('star_difficulty: Error finding game modes in json of beatmap '
                         + beatmap.id_ + '.', err)
        return -1
    max_difficulty = -1
    for difficulty, mode in zip(difficulties, game_modes):
        if mode == 0 and max_difficulty < difficulty:
            max_difficulty = difficulty
    return max_difficulty


def ok_creator(beatmap):
    return ok_pp_rank(beatmap) or ok_kudosu(beatmap) or ok_maps(beatmap)


def ok_pp_rank(beatmap):
    try:
        pp_rank = PP_RANK_.search(beatmap.creator).group(1)
        return int(pp_rank) <= MIN_PP_RANK
    except Exception as err:
        logger.error_msg('ok_pp_rank: Could not find pp_rank regular expression in creator of beatmap '
                         + beatmap.id_ + '.', err)
        return False


def ok_kudosu(beatmap):
    return False


def ok_maps(beatmap):
    return ok_ranked(beatmap) or ok_non_ranked(beatmap)


def ok_ranked(beatmap):
    try:
        ranked = RANKED_.search(beatmap.profile).group(1)
    except (AttributeError, IndexError):
        ranked = 0

    return int(ranked) >= MIN_RANKED


def ok_non_ranked(beatmap):
    try:
        pending = PENDING_.search(beatmap.profile).group(1)
    except (AttributeError, IndexError):
        pending = 0
    try:
        graveyarded = GRAVEYARDED_.search(beatmap.profile).group(1)
    except (AttributeError, IndexError):
        graveyarded = 0

    return int(pending) + int(graveyarded) >= MIN_NON_RANKED


def ok_favourited(beatmap):
    return favourited_times(beatmap) >= MIN_FAVOURITED


def favourited_times(beatmap):
    try:
        number = FAVOURITED_TIMES_.findall(beatmap.all_maps)[beatmap.index]
        return int(number)
    except Exception as err:
        logger.error_msg('favourited_times: Could not find favourited times regular expression in all_maps of beatmap '
                         + beatmap.id_ + '.', err)
        return 0


def filter_maps(beatmaps):
    logger.error_msg("filter_maps: Filtering maps.", None)
    logger.error_msg("filter_maps: Before filtering: " + str(len(beatmaps)) + " maps.", None)
    for i in range(len(beatmaps) - 1, -1, -1):
        if beatmaps[i].id_ not in DATABASE and ok_difficulty(beatmaps[i]) and\
                (ok_creator(beatmaps[i]) or ok_favourited(beatmaps[i])):
            continue
        else:
            beatmaps.pop(i)
    logger.error_msg("filter_maps: After filtering: " + str(len(beatmaps)) + " maps.", None)