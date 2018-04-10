# -*- coding: utf-8 -*-
"""

"""

from typing import List
from datetime import datetime

import luigi

from src.save_rank import CleanUpTask


buffer = None

def input(date_hours: List[datetime]):



class RunAll(luigi.Task):
    ''' Dummy task that triggers execution of a other tasks'''
    def requires(self):
        for window in [3, 7, 14]:
            for d in xrange(10): # guarantee that aggregations were run for the past 10 days
               yield AggregationTask(datetime.date.today() - datetime.timedelta(d), window)

