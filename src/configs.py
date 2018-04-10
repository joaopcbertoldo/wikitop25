# -*- coding: utf-8 -*-
"""
configs.py
    Configurations of the application.
        Environment configs (folders, files, paths)
        Defaults values/formats (date/hour formats, rank size, json)
        Options of behavior.
"""

import re
import sys


# ---------------------------------------- find the project's absolute abspath -----------------------------------------
# get this module's abspath
configs_path = sys.modules[__name__].__file__

# regex pattern to find everything before the project's name
pattern = re.compile(r'(.)*\\wikitop25\\')

# result of the regex
wikitop25_abs_path = re.match(pattern, configs_path).group()


# --------------------------------------- container classes with the configs -------------------------------------------

# environment
class Environment:
    """
    Environment configurations.
        Temp folders absolute paths.
        Black list folder/files absolute paths.
        Rank folder absolute path.
    """

    # project's abspath
    wikitop25_abs_path = wikitop25_abs_path

    # abspath of the temp folder
    temp_abs_path = wikitop25_abs_path + r'temp\\'

    # abspath of the temp\download folder
    temp_download_abs_path = temp_abs_path + r'download\\'

    # abspath of temp\rank_pickle folder
    temp_rank_pickle_abs_path = temp_abs_path + r'rank_pickle\\'

    # abspath of ranks folder
    ranks_abs_path = wikitop25_abs_path + r'ranks\\'

    # black list folder
    black_list_folder = wikitop25_abs_path + r'src\\black_list\\'

    # black list original file`s name and abspath
    black_list_original_name = 'blacklist_domains_and_pages'
    black_list_original_path = black_list_folder + black_list_original_name

    # black list pickle file`s name and abspath
    black_list_pickle_name = 'black_list_dict.pickle'
    black_list_pickle_path = black_list_folder + black_list_pickle_name


# Defaults
class Defaults:
    """
    Defaults of the application.
        date format
        hour format
        date hour format
        rank size/augmented rank size
        json indentation
    """

    # date format (datetime, human readable, example)
    date_format = "%Y-%m-%d"
    date_format_h = "YYYY-MM-DD"
    date_format_ex = "2018-04-08"

    # hour format (human readable, example)
    hour_format_h = "hh (24h)"
    hour_format_ex = "20"

    # date hour format (datetime, human readable)
    date_hour_format = "%Y-%m-%d-%HH"
    date_hour_format_h = "%Y-%m-%d at %Hh"

    # rank size
    rank_size = 25

    # augmented rank size (size used to build the ranks, to compensate the fact that it is filtered later)
    augmented_rank_size = 50

    # json indentation
    json_indentation = 4


# Options
class Options:
    """Options concerning the application's behavior."""

    # filter main page --> whether the Main_Page page should be banned (it is often the top 1 if not)
    filter_main_page = True

    # luigi scheduler --> whether to use or not a local scheduler
    use_local_scheduler = False

