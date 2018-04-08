import argparse
from datetime import datetime

import src.defaults as defaults
from src.main import main


# validate the date input
def valid_date(s):
    try:
        # conversion
        return datetime.strptime(s, defaults.date_format).date()

    except ValueError:
        # error message
        msg = f"Not a valid date: '{s}'." \
              + f"The correct format is '{defaults.date_format_h}' (ex: '{defaults.date_format_ex}')."
        # raise
        raise argparse.ArgumentTypeError(msg)


# arg parser
parser = argparse.ArgumentParser(description='Computes the top 25 pages for each sub-domain in Wikipedia.')

# date - help msg
help_msg = f"Date of the date to analyze. Format: '{defaults.date_format_h}'. Ex: '{defaults.date_format_ex}'."
help_msg += "Default: current date."
# date - arg
parser.add_argument('date', type=valid_date, nargs='?', default=None, help=help_msg)

# hour - help msg
help_msg = f"Hour of the hour to analyze. Format: '{defaults.hour_format_h}'. Ex: '{defaults.hour_format_ex}'."
help_msg += "Default: current hour."
# hour - arg
parser.add_argument('hour', type=int, choices=range(24), nargs='?', default=None, help=help_msg)

# debug
parser.add_argument('--debug', action='store_true')

# namespace
ns = parser.parse_args()


# check that both or neither are given
if bool(ns.date) ^ (ns.hour != None):
    parser.error("'date' and 'hour' must be given together (or neither of them should be given).")


# default case
if not ns.date and (ns.hour == None):
    now = datetime.now()
    ns.date = now.date()  # date
    ns.hour = now.time().hour  # hour


# echo
if ns.debug:
    print(50 * '.')
    print('ECHO')
    print(ns)
    print(50 * '.')


# main
if __name__ == '__main__':
    main(ns)
