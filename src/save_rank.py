# -*- coding: utf-8 -*-
"""

"""
import json
from typing import Dict
from datetime import datetime

import luigi
import pickle
from luigi.target import Target
from luigi import format

from src.configs import Defaults as defaults
from src.configs import Environment as env
from src.rank import Rank
from src.compute_rank import ComputeRankTask


# Save Rank Task
class SaveRankTask(luigi.Task):

    # date hour parameter
    date_hour = luigi.DateHourParameter()

    # requires
    def requires(self):
        return ComputeRankTask(self.date_hour)

    # run
    def run(self):
        # check existence
        if self.output().exists():
            return

        # load the ranks from the input
        with open(self.input().path, 'rb') as f:
            ranks = pickle.load(f)
            #ranks: Dict[str, Rank] = pickle.load(f)

        # for each domain
        for domain, rank in ranks.items():

            # get the items in dict format
            dictionized_items = rank.dictionized_items

            # replace the rank by them
            ranks[domain] = dictionized_items

        # write it to the json
        with self.output().open('w') as f:
            json.dump(ranks, f, indent=defaults.json_indentation)

    # output
    def output(self) -> Target:
        # filename
        filename = self.date_hour.strftime(defaults.date_hour_format + '.json')

        # abs path
        abspath = env.ranks_abs_path + filename

        # target
        target = luigi.LocalTarget(abspath, format=format.UTF8)
        return target


# test
def _test():
    # date-hour's
    dt1 = datetime(year=2017, month=3, day=18, hour=12)
    dt2 = datetime(year=2018, month=3, day=18, hour=12)

    # tasks
    t1 = SaveRankTask(dt1)
    #t2 = SaveRankTask(dt2)

    # gather tasks
    tasks = [t1]
    # tasks = [t1, t2]

    # build
    luigi.build(tasks, worker_scheduler_factory=None, local_scheduler=True)


# run the test
if __name__ == '__main__':
    _test()
    pass
