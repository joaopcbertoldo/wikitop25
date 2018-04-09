# -*- coding: utf-8 -*-
"""

"""

import gzip
from typing import List, Dict
from datetime import datetime

import luigi
from luigi.target import Target
from luigi import format
from tqdm import tqdm

from src.rank import Rank
from src.configs import Defaults as defaults
from src.configs import Environment as env
from src.black_list import BlackList
from src.download import DownloadTask


def _transform(line: bytes) -> List:
    return line.decode('utf-8').split()[0:3]


def extract_content(dt: datetime) -> List[List[str]]:

    fpath = download_pageviews(dt)

    with gzip.open(fpath, 'rb') as f:
        content = [_transform(line) for line in f.readlines()]

    return content


def sort_by_domain(content: List[List[str]]) -> Dict[str, List]:
    by_domain = {}

    for element in content:
        domain = element[0]
        page = element[1]
        pageview = int(element[2])

        info = [page, pageview]

        if domain in by_domain:
            by_domain[domain].append(info)
        else:
            by_domain[domain] = [info]

    return by_domain


def apply_black_list_filter(to_be_ranked_by_domain: Dict[str, List]):
    black_list = black_list.load()

    for domain in black_list:
        to_be_ranked = to_be_ranked_by_domain.get(domain, None)
        banned_pages = black_list[domain]

        if not to_be_ranked:
            continue

        for page in banned_pages:
            if not page:
                # remove all from that domain
                to_be_ranked_by_domain.pop(domain)
            else:
                def condition(e: List):
                    return e[0] == page
                try:
                   i = next(i for i, e in enumerate(to_be_ranked) if condition(e))
                   to_be_ranked.pop(i)
                except:
                    continue
                # to_be_ranked_by_domain[domain] = list(filter(f, to_be_ranked))


def rank_by_domain(to_be_ranked_by_domain: Dict[str, List]) -> Dict[str, Rank]:
    ranks = {}
    for domain in tqdm(to_be_ranked_by_domain.keys()):
        r = Rank(name=domain, maxlen=defaults.rank_size)
        pages = to_be_ranked_by_domain[domain]

        for page in pages:
            name = page[0]
            score = page[1]
            r.push(content=name, score=score)

        ranks[domain] = r.tuples

    return ranks


class ComputeRankTask(luigi.Task):

    # date hour parameter
    date_hour = luigi.DateHourParameter()

    # requires
    def requires(self):
        return DownloadTask(self.date_hour)

    # run
    def run(self):
        if self.output().exists():
            return
        pass

    # output
    def output(self) -> Target:
        filename = self.date_hour.strftime(defaults.date_hour_format)
        abspath = env.temp_rank_pickle_abs_path + filename
        target = luigi.LocalTarget(abspath, format=format.Nop)
        return target


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


if __name__ == '__main__':
    _test()
    pass

