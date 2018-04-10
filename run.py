# -*- coding: utf-8 -*-
"""
run.py
    Manages the command parsing, validates the inputs and calls the application's main.
    It is a separation layer from the application logic so that it can work supposing valid inputs.
    Important: before running this script, one should:
        a) run luigi daemon --> run the command "luigid" on another terminal
            - in this case, see the tasks dashboard at http://localhost:8082
        b) go to src/configs, go to the class Options and change use_local_scheduler's value to False
"""

import argparse
import datetime as dt_module
from datetime import datetime, time

from src.configs import Defaults as defaults
from src.main import main


# wikipedia's earliest date-hour available for the pageviews
WIKIPEDIA_EARLIEST_PAGEVIEWS = datetime(2015, 5, 1, 1)

# ------------------------------------------------- aux ----------------------------------------------------------------
# auxiliary function to validate a date given by a string (used in the parsers)


# validate the date input
def valid_date(s: str):
    try:
        # conversion
        return datetime.strptime(s, defaults.date_format).date()

    except ValueError:
        # error message
        msg = f"Not a valid date: '{s}'." \
              + f"The correct format is '{defaults.date_format_h}' (ex: '{defaults.date_format_ex}')."
        # raise a arparser's exception
        raise argparse.ArgumentTypeError(msg)


# -------------------------------------------- general parser ----------------------------------------------------------
# construction of the general parser of the script

# arg parser (the main parser)
parser = argparse.ArgumentParser(prog='wikitop25',
                                 description='Computes the top 25 pages for each sub-domain in Wikipedia.')

# subparsers
subparsers = parser.add_subparsers(help='Commands', dest='command')

# single command's parser
desc = 'Get single date and hour as input.'
single_parser = subparsers.add_parser('single', description=desc, help=desc)

# range command's parser
desc = 'Get a range of dates and hours as input (executed once for each date and hour in the range).'
range_parser = subparsers.add_parser('range', description=desc, help=desc)

# debug option
parser.add_argument('--debug', action='store_true')


# -------------------------------------------- single date parser ------------------------------------------------------
# construction of the parser for the single command

# date - help msg
help_msg = f"Date to analyze. "
help_msg += f"Format: '{defaults.date_format_h}'. Ex: '{defaults.date_format_ex}'. "
help_msg += "Default: current date."

# date - add arg
single_parser.add_argument('date', type=valid_date, nargs='?', default=None, help=help_msg)

# hour - help msg
help_msg = "Hour of the date to analyze. "
help_msg += f"Format: '{defaults.hour_format_h}'. Ex: '{defaults.hour_format_ex}'."
help_msg += "Default: current hour."

# hour - add arg
single_parser.add_argument('hour', metavar='hour', type=int, choices=range(24), nargs='?', default=None, help=help_msg)


# -------------------------------------------- single post-parsing -----------------------------------------------------
# post parsing behavior for the single command
def single_post_parsing(ns):
    global single_parser

    # check that both or neither are given
    if bool(ns.date) ^ (ns.hour != None):
        single_parser.error("'date' and 'hour' must be given together (or neither of them should be given).")

    # default case (1h before the current) -- the current hour could fail because it might not be available yet
    if not ns.date and (ns.hour == None):
        now = datetime.now()
        ns.date = now.date()  # date
        ns.hour = now.time().hour - 1  # hour

    # the date-hour to be processed
    ns.dt = datetime.combine(ns.date, time(hour=ns.hour))

    # check that dh is after wikipedia's earliest pageviews (error message if not)
    if not ns.dt >= WIKIPEDIA_EARLIEST_PAGEVIEWS:
        limitstr = WIKIPEDIA_EARLIEST_PAGEVIEWS.strftime(defaults.date_hour_format_h)
        dtstr = ns.dt.strftime(defaults.date_hour_format_h)
        err_msg = f"The instant to process must be after or equal to the the earliest available info ({limitstr}). "
        err_msg += f"\n\tGiven: {dtstr}"
        single_parser.error(err_msg)

    # now
    dtnow = datetime.now()

    # check that dh is before now (error message if not)
    if not ns.dt <= dtnow:
        nowstr = dtnow.strftime(defaults.date_hour_format_h)
        dtstr = ns.dt.strftime(defaults.date_hour_format_h)
        err_msg = f"The instant to process must be before or equal to the current time ({nowstr}). "
        err_msg += f"\n\tGiven: {dtstr}"
        single_parser.error(err_msg)


# -------------------------------------------------- range parser ------------------------------------------------------
# construction of the range parser

# begin_date - help msg
help_msg = "Date of the FIRST date-hour to analyze (beginning of the range). "
help_msg += f"Format: '{defaults.date_format_h}'. Ex: '{defaults.date_format_ex}'."

# begin_date - add arg
range_parser.add_argument('begin_date', type=valid_date, help=help_msg)

# begin_hour - help msg
help_msg = "Hour of the FIRST date-hour to analyze (beginning of the range). "
help_msg += f"Format: '{defaults.hour_format_h}'. Ex: '{defaults.hour_format_ex}'."

# begin_hour - add arg
range_parser.add_argument('begin_hour', metavar='begin_hour', type=int, choices=range(24), help=help_msg)

# end_date - help msg
help_msg = "Date of the LAST date-hour to analyze (end of the range). "
help_msg += f"Format: '{defaults.date_format_h}'. Ex: '{defaults.date_format_ex}'."

# end_date - add arg
range_parser.add_argument('end_date', type=valid_date, help=help_msg)

# end_hour - help msg
help_msg = "Hour of the LAST date-hour to analyze (end of the range). "
help_msg += f"Format: '{defaults.hour_format_h}'. Ex: '{defaults.hour_format_ex}'."

# end_hour - add arg
range_parser.add_argument('end_hour', metavar='end_hour', type=int, choices=range(24), help=help_msg)


# ------------------------------------------- range post-parsing -------------------------------------------------------
# post parsing behavior for the range command
def range_post_parsing(ns):
    # range parser
    global range_parser

    # beginning (first date-hour)
    ns.dt0 = datetime.combine(ns.begin_date, time(hour=ns.begin_hour))

    # end (last date-hour)
    ns.dtN = datetime.combine(ns.end_date, time(hour=ns.end_hour))

    # check that end is after beginning (error message if not)
    if not ns.dtN > ns.dt0:
        dt0str = ns.dt0.strftime(defaults.date_hour_format_h)
        dtNstr = ns.dtN.strftime(defaults.date_hour_format_h)
        err_msg = "The end must be after than the beginning."
        err_msg += "\n\tGiven: \n"
        err_msg += f"\t\tbegining = {dt0str} \n"
        err_msg += f"\t\tend = {dtNstr}"
        range_parser.error(err_msg)

    # now
    dtnow = datetime.now()

    # check that the end is before now (error message if not)
    if not ns.dtN <= dtnow:
        nowstr = dtnow.strftime(defaults.date_hour_format_h)
        dtNstr = ns.dtN.strftime(defaults.date_hour_format_h)
        err_msg = f"The end must be before or equal to the current time ({nowstr}). "
        err_msg += "\n\tGiven: \n"
        err_msg += f"\t\tend = {dtNstr}"
        range_parser.error(err_msg)

    # check that the beginning is after wikipedia's earliest pageviews (error message if not)
    if not ns.dt0 >= WIKIPEDIA_EARLIEST_PAGEVIEWS:
        limitstr = WIKIPEDIA_EARLIEST_PAGEVIEWS.strftime(defaults.date_hour_format_h)
        dtstr = ns.dt.strftime(defaults.date_hour_format_h)
        err_msg = f"The instant to process must be after or equal to the the earliest available info ({limitstr}). "
        err_msg += f"\n\tGiven: {dtstr}"
        range_parser.error(err_msg)

    # range of datetime-hours to process (between begin and end included)
    ns.dt_range = list()

    # count of hours after dt0
    i = 0
    while True:

        # compute current dh
        dt = ns.dt0 + dt_module.timedelta(hours=i)

        # append it to the range
        ns.dt_range.append(dt)

        # break if it is dtN
        if dt == ns.dtN:
            break

        # increment
        i += 1


# -------------------------------------------- parsing -----------------------------------------------------------------
# namespace (parse the args)
ns = parser.parse_args()

# check if the command was given (error message if not)
if not ns.command:
    parser.error('No command was passed. Call <<python run.py -h>> for help.')

# echo
if ns.debug:
    print(50 * '.')
    print('ECHO parsing')
    print(ns)
    print(50 * '.')


# -------------------------------------------- post-parsing ------------------------------------------------------------

# switch of functions (post processing behavior)
switch = {
    'single': single_post_parsing,
    'range': range_post_parsing,
}

# call the post parsing action
post_processing = switch[ns.command](ns)

# echo
if ns.debug:
    print(50 * '.')
    print('ECHO post processing')
    print(ns)
    print(50 * '.')


# main
if __name__ == '__main__':
    main(ns)
