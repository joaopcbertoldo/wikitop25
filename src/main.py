# -*- coding: utf-8 -*-
"""

"""
from datetime import datetime

import luigi

from src.configs import Options as opt
from src.setup_environment import setup_temp
from src.workflow import create_tasks

# setup the temp folder and sub folders
setup_temp()


def main(ns):

    if ns.command == 'single':
        tasks = create_tasks([ns.dt])

    elif ns.command == 'range':
        tasks = create_tasks(ns.dt_range)

    # build
    luigi.build(tasks, worker_scheduler_factory=None, local_scheduler=opt.use_local_scheduler)


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

    # namespace
    class Ns:
        comamnd = 'single'
        dt = datehour

    # call the main
    main(Ns())
