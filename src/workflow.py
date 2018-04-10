# -*- coding: utf-8 -*-
"""

"""

from typing import List
from datetime import datetime

import luigi

from src.save_rank import SaveRankTask, CleanUpTask


def create_tasks(date_hours: List[datetime]) -> List[luigi.Task]:

    buffer = []

    # iterate through the date hours given
    for dh in date_hours:

        # create a save task
        svtask = SaveRankTask(dh)

        # ignore it if it is already done
        done = svtask.output().exists()
        if done:
            continue

        # create a clean up task
        cutask = CleanUpTask(dh)

        # add it to the buffer
        buffer.append(cutask)

    return buffer
