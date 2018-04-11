# -*- coding: utf-8 -*-
"""
main.py
    Gets a set of command/inputs and run the application with them by calling luigi's scheduler with the tasks.
"""
import luigi

from src.configs import Options as opt
from src import setup_environment
from src.workflow import create_tasks


# setup the environment
setup_environment.run()


# main
def main(ns):
    """Main will get a command and its necessary inputs, create the tasks and send to luigi's schedule."""

    # command single
    if ns.command == 'single':
        tasks = create_tasks([ns.dt])

    # command range
    elif ns.command == 'range':
        tasks = create_tasks(ns.dt_range)

    # build (calling luigi's scheduler)
    luigi.build(tasks, worker_scheduler_factory=None, local_scheduler=opt.use_local_scheduler)


# test purposes
if __name__ == '__main__':
    print('testing...')
    from random import randint as ri
    from datetime import datetime

    # create a random date and hour
    datehour = datetime(
        year=ri(2016, 2018),
        month=ri(1, 12),
        day=ri(1, 28),
        hour=ri(0, 23)
    )

    print('date:', str(datehour))

    # namespace
    class Ns:
        command = 'single'
        dt = datehour

    # call the main
    main(Ns())
