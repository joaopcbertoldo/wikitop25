# -*- coding: utf-8 -*-
"""
This module manages the command line that calls the application and parses the inputs.

It is a separation layer from the application, passing to it uniquely valid inputs.
"""

import argparse
import datetime as dt_module
from datetime import datetime, time

from src.configs import Defaults as defaults
from src.main import main


WIKIPEDIA_EARLIEST_PAGEVIEWS = datetime(2015, 5, 1, 1)

# ------------------------------------------------- aux ----------------------------------------------------------------

# validate the date input
def valid_date(s: str):
    try:
        # conversion
        return datetime.strptime(s, defaults.date_format).date()

    except ValueError:
        # error message
        msg = f"Not a valid date: '{s}'." \
              + f"The correct format is '{defaults.date_format_h}' (ex: '{defaults.date_format_ex}')."
        # raise
        raise argparse.ArgumentTypeError(msg)


# -------------------------------------------- general parser ----------------------------------------------------------
# arg parser
parser = argparse.ArgumentParser(prog='wikitop25',
                                 description='Computes the top 25 pages for each sub-domain in Wikipedia.')

# subparsers
subparsers = parser.add_subparsers(help='Commands', dest='command')

# single date parser
desc = 'Get single date and hour as input.'
single_parser = subparsers.add_parser('single', description=desc, help=desc)

# range of dates parser
desc = 'Get a range of dates and hours as input (executed once for each date and hour in the range).'
range_parser = subparsers.add_parser('range', description=desc, help=desc)

# debug
parser.add_argument('--debug', action='store_true')


# -------------------------------------------- single date parser ------------------------------------------------------
# date - help msg
help_msg = f"Date to analyze. "
help_msg += f"Format: '{defaults.date_format_h}'. Ex: '{defaults.date_format_ex}'. "
help_msg += "Default: current date."

# date - arg
single_parser.add_argument('date', type=valid_date, nargs='?', default=None, help=help_msg)

# hour - help msg
help_msg = "Hour of the date to analyze. "
help_msg += f"Format: '{defaults.hour_format_h}'. Ex: '{defaults.hour_format_ex}'."
help_msg += "Default: current hour."

# hour - arg
single_parser.add_argument('hour', metavar='hour', type=int, choices=range(24), nargs='?', default=None, help=help_msg)


# -------------------------------------------- single post-parsing -----------------------------------------------------
def single_post_parsing(ns):
    global single_parser

    # check that both or neither are given
    if bool(ns.date) ^ (ns.hour != None):
        single_parser.error("'date' and 'hour' must be given together (or neither of them should be given).")

    # default case
    if not ns.date and (ns.hour == None):
        now = datetime.now()
        ns.date = now.date()  # date
        ns.hour = now.time().hour  # hour

    # datetime
    ns.dt = datetime.combine(ns.date, time(hour=ns.hour))

    # dt after wikipedia's earliest pageviews
    if not ns.dt >= WIKIPEDIA_EARLIEST_PAGEVIEWS:
        limitstr = WIKIPEDIA_EARLIEST_PAGEVIEWS.strftime(defaults.date_hour_format_h)
        dtstr = ns.dt.strftime(defaults.date_hour_format_h)
        err_msg = f"The instant to process must be after or equal to the the earliest available info ({limitstr}). "
        err_msg += f"\n\tGiven: {dtstr}"
        single_parser.error(err_msg)

    # now
    dtnow = datetime.now()

    # dt before now
    if not ns.dt <= dtnow:
        nowstr = dtnow.strftime(defaults.date_hour_format_h)
        dtstr = ns.dt.strftime(defaults.date_hour_format_h)
        err_msg = f"The instant to process must be before or equal to the current time ({nowstr}). "
        err_msg += f"\n\tGiven: {dtstr}"
        single_parser.error(err_msg)


# -------------------------------------------- range of dates parser ---------------------------------------------------
# begin_date - help msg
help_msg = "Date of the FIRST date-hour to analyze (beginning of the range). "
help_msg += f"Format: '{defaults.date_format_h}'. Ex: '{defaults.date_format_ex}'."

# begin_date - arg
range_parser.add_argument('begin_date', type=valid_date, help=help_msg)

# begin_hour - help msg
help_msg = "Hour of the FIRST date-hour to analyze (beginning of the range). "
help_msg += f"Format: '{defaults.hour_format_h}'. Ex: '{defaults.hour_format_ex}'."

# begin_hour - arg
range_parser.add_argument('begin_hour', metavar='begin_hour', type=int, choices=range(24), help=help_msg)

# end_date - help msg
help_msg = "Date of the LAST date-hour to analyze (end of the range). "
help_msg += f"Format: '{defaults.date_format_h}'. Ex: '{defaults.date_format_ex}'."

# end_date - arg
range_parser.add_argument('end_date', type=valid_date, help=help_msg)

# end_hour - help msg
help_msg = "Hour of the LAST date-hour to analyze (end of the range). "
help_msg += f"Format: '{defaults.hour_format_h}'. Ex: '{defaults.hour_format_ex}'."

# end_hour - arg
range_parser.add_argument('end_hour', metavar='end_hour', type=int, choices=range(24), help=help_msg)


# --------------------------------------- range of dates post-parsing --------------------------------------------------
def range_post_parsing(ns):
    global range_parser

    # beginning
    ns.dt0 = datetime.combine(ns.begin_date, time(hour=ns.begin_hour))

    # end
    ns.dtN = datetime.combine(ns.end_date, time(hour=ns.end_hour))

    # end after begining
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

    # end before now
    if not ns.dtN <= dtnow:
        nowstr = dtnow.strftime(defaults.date_hour_format_h)
        dtNstr = ns.dtN.strftime(defaults.date_hour_format_h)
        err_msg = f"The end must be before or equal to the current time ({nowstr}). "
        err_msg += "\n\tGiven: \n"
        err_msg += f"\t\tend = {dtNstr}"
        range_parser.error(err_msg)

    # beginning after wikipedia's earliest pageviews
    if not ns.dt0 >= WIKIPEDIA_EARLIEST_PAGEVIEWS:
        limitstr = WIKIPEDIA_EARLIEST_PAGEVIEWS.strftime(defaults.date_hour_format_h)
        dtstr = ns.dt.strftime(defaults.date_hour_format_h)
        err_msg = f"The instant to process must be after or equal to the the earliest available info ({limitstr}). "
        err_msg += f"\n\tGiven: {dtstr}"
        range_parser.error(err_msg)

    # range of datetimes to process
    ns.dt_range = list()

    i = 0
    while True:
        dt = ns.dt0 + dt_module.timedelta(hours=i)
        ns.dt_range.append(dt)

        if dt ==ns.dtN:
            break

        i += 1


# -------------------------------------------- parsing -----------------------------------------------------------------
# namespace
ns = parser.parse_args()

# no command case
if not ns.command:
    parser.error('No command was passed. Call <<python run.py -h>> for help.')

# echo
if ns.debug:
    print(50 * '.')
    print('ECHO parsing')
    print(ns)
    print(50 * '.')


# -------------------------------------------- post-parsing ------------------------------------------------------------

# switch of functions
switch = {
    'single': single_post_parsing,
    'range': range_post_parsing,
}

# call
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
