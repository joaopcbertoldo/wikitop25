import os.path
import re


# find the project's absolute path
abs_path = os.path.abspath('.')
pattern = re.compile(r'(.)*\\wikitop25\\')
result = re.match(pattern, abs_path)
wikitop25_abs_path = result.group()


class Environment:
    wikitop25_abs_path = wikitop25_abs_path
    temp_abs_path = wikitop25_abs_path + r'temp\\'

    black_list_folder = wikitop25_abs_path + r'src\\black_list\\'

    black_list_original_name = 'blacklist_domains_and_pages'
    black_list_original_path = black_list_folder + black_list_original_name

    black_list_pickle_name = 'black_list_dict.pickle'
    black_list_pickle_path = black_list_folder + black_list_pickle_name


class Defaults:
    date_format = "%Y-%m-%d"
    date_format_h = "YYYY-MM-DD"
    date_format_ex = "2018-04-08"

    hour_format_h = "hh (24h)"
    hour_format_ex = "20"

    date_hour_format = "%Y-%m-%d at %Hh"


class Templates:
    pageviews_url = 'https://dumps.wikimedia.org/other/pageviews/%Y/%Y-%m/pageviews-%Y%m%d-%H0000.gz'

