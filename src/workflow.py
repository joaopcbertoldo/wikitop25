# -*- coding: utf-8 -*-
"""
workflow.py
    Creates the tasks to be run if necessary (some are discarded as their results have already been computed).
"""

from typing import List
from datetime import datetime

import luigi

from src.save_rank import SaveRankTask, CleanUpTask


# create tasks
def create_tasks(date_hours: List[datetime]) -> List[luigi.Task]:
    """
    Gets a list of date-hours to analyze and create luigi tasks to be run if necessary
    (that is, when their results do not exist yet).
    """

    # list of the tasks to be executed (some are discarded as their results have already been computed)
    buffer = []

    # iterate through the given date-hours
    for dh in date_hours:

        # create a save task
        svtask = SaveRankTask(dh)

        # ignore it if it is already done (existing output)
        done = svtask.output().exists()
        if done:
            continue

        # create a clean up task --> because it is the last one in the workflow
        cutask = CleanUpTask(dh)

        # add it to the buffer
        buffer.append(cutask)

    return buffer
