# -*- coding: utf-8 -*-
"""
download.py
    Defines the DownloadTask (first in the workflow) and auxiliary stuff for it.
    DownloadTask: downloads the gz file from wikimedia (via http request), decompresses it, decodes it in utf-8
                  and saves the result in a txt file.
"""

import gzip
import requests
from datetime import datetime

import luigi
from luigi import format
from luigi.target import Target

from src.configs import Environment as env


# template url for wikipedia's api
pageviews_url_template = 'https://dumps.wikimedia.org/other/pageviews/%Y/%Y-%m/pageviews-%Y%m%d-%H0000.gz'


# create url
def create_url(dt: datetime) -> str:
    """Create the wikipedia url to download the pageviews for the given datetime."""

    # replace values in the template
    url = dt.strftime(pageviews_url_template)

    # ret
    return url


# Download Target Meta Data
class DownloadTargetMetaData:
    """Gathers several practical infos concerning a download target's meta data."""

    def __init__(self, dh: datetime):
        """dh is the date time containing the date and hour of the rank to be computed."""
        # date-hour
        self.dh: datetime = dh

        # url (to the pageviews)
        self.url: str = create_url(self.dh)

        # name of the downloaded file
        self.name: str = self.url.split("/")[-1]

        # abs abspath of the downloaded file
        self.abspath: str = env.temp_download_abs_path + self.name + '.txt'


# task
class DownloadTask(luigi.Task):
    """Task that downloads a pageview gz file, reads it and saves it in txt."""

    # date hour parameter
    date_hour = luigi.DateHourParameter()

    # init
    def __init__(self, *args, **kwargs):
        luigi.Task.__init__(self, *args, **kwargs)

        # the metadata of the download's file
        self._filemeta = DownloadTargetMetaData(self.date_hour)

    # run
    def run(self):

        # check existence of the target - for test purposes
        if self.output().exists():
            return

        # get the info from internet
        response = requests.get(self._filemeta.url)

        # get the content
        # decompress it (from gz)
        # decode the bytes in utf-8 (str as result)
        txt = gzip.decompress(response.content).decode('utf-8')

        # open txt file
        with self.output().open("w") as f:

            # write to it
            f.write(txt)

    # output - local target (txt)
    def output(self) -> Target:
        # abspath
        abspath = self._filemeta.abspath

        # target (format UTF8 is important!!!)
        target = luigi.LocalTarget(abspath, format=format.UTF8)

        # ret
        return target


# test the task
def _test_task():
    # get two dates
    dt1 = datetime(year=2017, month=3, day=1, hour=0)
    dt2 = datetime(year=2018, month=3, day=18, hour=12)

    # create the tasks
    t1 = DownloadTask(dt1)
    t2 = DownloadTask(dt2)

    # gather them
    tasks = [t1, t2]

    # build
    luigi.build(tasks, worker_scheduler_factory=None, local_scheduler=True)


# test purposes
if __name__ == '__main__':
    _test_task()
    pass
