# -*- coding: utf-8 -*-
"""
save_rank.py
    Defines tasks SaveRankTask (third one) and CleanUpTask (fourth and last one).
        SaveRankTask:
            Gets a computed rank, transforms it in a json and save it.
        CleanUpTask:
            Deletes temporary files from the intermediate tasks (Download and ComputeRank).
"""
import os
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
    """
    Gets the computed ranks as Rank objects, transform them in a list of items (for each domain) where each
    item is transformed in a dictionary, than that is outputted as a json in a txt file.
    """

    # date hour parameter
    date_hour = luigi.DateHourParameter()

    # requires ComputeRankTask
    def requires(self):
        return ComputeRankTask(self.date_hour)

    # run
    def run(self):
        # check existence - for test purposes
        if self.output().exists():
            return

        # load the ranks from the input (the binary file)
        with open(self.input().path, 'rb') as f:
            ranks: Dict[str, Rank] = pickle.load(f)

        # for each domain
        for domain, rank in ranks.items():

            # get the items in dict format
            dictionized_items = rank.dictionized_items

            # replace the rank by them
            ranks[domain] = dictionized_items

        # write it to the json file
        with self.output().open('w') as f:
            json.dump(ranks, f, indent=defaults.json_indentation)

    # output - local target (txt, json)
    def output(self) -> Target:
        # filename
        filename = self.date_hour.strftime(defaults.date_hour_format + '.json')

        # abs path
        abspath = env.ranks_abs_path + filename

        # target (utf8 is important!!!!)
        target = luigi.LocalTarget(abspath, format=format.UTF8)
        return target


# Clean Temp Files Task
class CleanUpTask(luigi.Task):
    """
    Deletes the temporary files from other tasks and replaces them with dummy files.
    dummy file --> empty file such that created tasks recognize that the task has been run (also human debugable).
    """

    # date hour parameter
    date_hour = luigi.DateHourParameter()

    # requires SaveRankTask
    def requires(self):
        return SaveRankTask(self.date_hour)

    # run
    def run(self):
        # path to the pickle file (from compute_rank)
        pickle_abspath = self.requires().input().path

        # path to the download's file
        download_abspath = self.requires().requires().input().path

        # delete these files and let dummy files in their places

        # delete pickle file (from compute_rank)
        if os.path.isfile(pickle_abspath):
            os.remove(pickle_abspath)

        # dummy file
        open(pickle_abspath, 'a').close()

        # delete download's file
        if os.path.isfile(download_abspath):
            os.remove(download_abspath)

        # dummy file
        open(download_abspath, 'a').close()


# test
def _test_save():
    # date-hour's
    dt1 = datetime(year=2017, month=3, day=18, hour=12)
    dt2 = datetime(year=2018, month=3, day=18, hour=12)

    # tasks
    t1 = SaveRankTask(dt1)
    # t2 = SaveRankTask(dt2)

    # gather tasks
    tasks = [t1]
    # tasks = [t1, t2]

    # build
    luigi.build(tasks, worker_scheduler_factory=None, local_scheduler=True)


def _test_cleanup():
    # date-hour's
    dt1 = datetime(year=2017, month=3, day=18, hour=19)

    # tasks
    t1 = CleanUpTask(dt1)

    # gather tasks
    tasks = [t1]

    # build
    luigi.build(tasks, worker_scheduler_factory=None, local_scheduler=False)


# run the test
if __name__ == '__main__':
    # _test_save()
    _test_cleanup()
    pass
