# -*- coding: utf-8 -*-
"""
compute_rank.py
    Defines the ComputeRankTask (second in the workflow).
    ComputeRankTask : gets the pageviews, compute the ranks per domain eliminating black listed pages and
                      saves the result in a pickle file.
"""

from datetime import datetime

import luigi
import pickle
from luigi.target import Target
from luigi import format
from tqdm import tqdm

from src.rank import Rank
from src.configs import Defaults as defaults
from src.configs import Environment as env
from src.configs import Options as opt
from src.black_list import BlackList
from src.download import DownloadTask


# Compute Rank Task
class ComputeRankTask(luigi.Task):
    """
    Gets a txt with all the pageviews, create a Rank object for each domain, push all the pages/pageviews
    to their respective ranks, than filters the ranks to eliminate blacklisted pages and saves in a pickle file
    as a dictionary of Rank objects per domain (as key).
    To avoid having a rank shorter than it should (because of eliminated pages), ranks a created with a bigger
    size first and then shortened to the correct size.
    """

    # date hour parameter
    date_hour = luigi.DateHourParameter()

    # requires the DownloadTask
    def requires(self):
        return DownloadTask(self.date_hour)

    # run
    def run(self):
        # check existence - for test purposes
        if self.output().exists():
            return

        # dict to store the ranks per domain
        ranks = {}

        # open the input file (txt)
        with self.input().open('r') as f:

            # in case of test, wrap the file with tqdm ('progressbar')
            iter = tqdm(f) if __name__ == '__main__' else f

            # iterate through the lines
            for line in iter:

                try:
                    # get the infos in the line
                    pieces = line.split()
                    domain = pieces[0]
                    page = pieces[1]
                    pageviews = pieces[2]

                    # convert the pageviews
                    pageviews = int(pageviews)

                except Exception:
                    continue

                # get the domain's rank if existent
                rank = ranks.get(domain, None)

                # check if it is ok
                if rank is None:
                    # if not, create one
                    rank = Rank(name=domain, maxlen=defaults.augmented_rank_size)

                    # and insert it in the dict
                    ranks[domain] = rank

                # push the content to it
                rank.push(page, pageviews)

        # get a black list
        bl = BlackList()

        # post validate the ranks
        for domain, rank in ranks.items():

            # validation func - filtering Main_Page
            if opt.filter_main_page:
                # func
                def validate(content):
                    # the black list (of this domain) must not have the content and cannot be 'Main_Page'
                    return bl.doesnt_have(domain, content) and content != 'Main_Page'

            # validation func - without filtering Main_Page
            else:
                # func
                def validate(content):
                    # the black list (of this domain) must not have the content
                    return bl.doesnt_have(domain, content)

            # post validate the contents (to filter the black listed pages)
            rank.post_validate(validate_fun=validate)

            # shorten the ranks to the real size
            rank.resize(defaults.rank_size)

        # dump the ranks dictionary in the output file
        with open(self.output().path, 'wb') as f:
            pickle.dump(ranks, f)

    # output - local target (binary, pickle)
    def output(self) -> Target:
        # filename
        filename = self.date_hour.strftime(defaults.date_hour_format + '.pickle')

        # abs path
        abspath = env.temp_rank_pickle_abs_path + filename

        # target - binary
        target = luigi.LocalTarget(abspath, format=format.Nop)
        return target


# test
def _test():
    # date-hour's
    dt1 = datetime(year=2017, month=3, day=1, hour=0)
    dt1p = datetime(year=2017, month=3, day=1, hour=1)

    # tasks
    t1 = ComputeRankTask(dt1)
    t1p = ComputeRankTask(dt1p)

    # gather tasks
    tasks = [t1, t1p]

    # build
    luigi.build(tasks, worker_scheduler_factory=None, local_scheduler=True)


# run the test
if __name__ == '__main__':
    _test()
    pass

