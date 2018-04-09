import re
import sys


# ------------------------------------ find the project's absolute abspath ------------------------------------
# get this module's abspath
configs_path = sys.modules[__name__].__file__

# regex pattern to find everything before the project's name
pattern = re.compile(r'(.)*\\wikitop25\\')

# result of the regex
wikitop25_abs_path = re.match(pattern, configs_path).group()


# environment
class Environment:

    # project's abspath
    wikitop25_abs_path = wikitop25_abs_path

    # abspath of the temp folder
    temp_abs_path = wikitop25_abs_path + r'temp\\'

    # abspath of the temp\download folder
    temp_download_abs_path = temp_abs_path + r'download\\'

    # black list folder
    black_list_folder = wikitop25_abs_path + r'src\\black_list\\'

    # black list original file`s name and abspath
    black_list_original_name = 'blacklist_domains_and_pages'
    black_list_original_path = black_list_folder + black_list_original_name

    # black list pickle file`s name and abspath
    black_list_pickle_name = 'black_list_dict.pickle'
    black_list_pickle_path = black_list_folder + black_list_pickle_name


class Defaults:
    date_format = "%Y-%m-%d"
    date_format_h = "YYYY-MM-DD"
    date_format_ex = "2018-04-08"

    hour_format_h = "hh (24h)"
    hour_format_ex = "20"

    date_hour_format = "%Y-%m-%d at %Hh"

    rank_size = 25
