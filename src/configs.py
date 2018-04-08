import os.path
import re


# find the project's absolute path
abs_path = os.path.abspath('.')
pattern = re.compile(r"(.)*\\wikitop25\\")
result = re.match(pattern, abs_path)
wikitop25_abs_path = result.group()


class Environment:
    wikitop25_abs_path = wikitop25_abs_path


class Defaults:
    date_format = "%Y-%m-%d"
    date_format_h = "YYYY-MM-DD"
    date_format_ex = "2018-04-08"

    hour_format_h = "hh (24h)"
    hour_format_ex = "20"

    date_hour_format = "%Y-%m-%d at %Hh"


class Templates:
    pageviews_url = 'https://dumps.wikimedia.org/other/pageviews/%Y/%Y-%m/pageviews-%Y%m%d-%H0000.gz'

