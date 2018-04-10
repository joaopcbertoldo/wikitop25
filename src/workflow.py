# -*- coding: utf-8 -*-
"""

"""

from typing import List
from datetime import datetime

import luigi

from src.save_rank import SaveRankTask, CleanUpTask


buffer = []


def create_main_task(date_hours: List[datetime]) -> luigi.Task:

    # iterate through the date hours given
    for dh in date_hours:

        # create a save task
        svtask = SaveRankTask(date_hours=dh)

        # ignore it if it is already done
        done = svtask.output().exists()
        if done:
            continue

        # create a clean up task
        cutask = CleanUpTask(date_hours=dh)

        # add it to the buffer
        buffer.append(cutask)

    return RunAll()


class RunAll(luigi.Task):
    """ Dummy task that triggers execution of a other tasks."""

    # requires
    def requires(self):
        global buffer
        for task in buffer:
            yield task
