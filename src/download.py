import os
import requests
import zlib
from datetime import datetime

import luigi
from luigi import format

from src.configs import Environment as env


pageviews_url_template = 'https://dumps.wikimedia.org/other/pageviews/%Y/%Y-%m/pageviews-%Y%m%d-%H0000.gz'


def create_url(dt: datetime) -> str:
    """Create the wikipedia url to download the pageviews for the given datetime."""

    # get the template
    template = pageviews_url_template

    # replace values
    url = dt.strftime(template)

    # ret
    return url


class DownloadTempFileMeta:

    def __init__(self, dt: datetime):
        self.dt: datetime = dt
        self.url: str = create_url(self.dt)
        self.name: str = self.url.split("/")[-1]
        self.path: str = env.temp_download_abs_path + self.name

    @property
    def exists(self) -> bool:
        exists = os.path.isfile(self.path)
        return exists


# for test purposes
def download_pageviews_job(url: str, file_path):
    # open file
    with open(file_path, "wb") as f:

        # get the info from internet
        r = requests.get(url)

        # write it in the file
        f.write(r.content)


# for test purposes
def download_pageviews(meta: DownloadTempFileMeta):
    """..."""

    if meta.exists:
        pass
    else:
        download_pageviews_job(meta.url, meta.path)


# for test purposes
def delete_job(file_path: str):
    os.remove(file_path)


# for test purposes
def delete_temp(meta: DownloadTempFileMeta):
    """..."""
    if meta.exists:
        delete_job(meta.path)
    else:
        pass


# task
class DownloadTask(luigi.Task):

    # date hour parameter
    date_hour = luigi.DateHourParameter()

    def __init__(self, *args, **kwargs):
        luigi.Task.__init__(self, *args, **kwargs)

        self._filemeta = DownloadTempFileMeta(self.date_hour)

    def run(self):

        # get the info from internet
        response = requests.get(self._filemeta.url)

        # decompressed content
        bytes_ = zlib.decompress(response.content, 15 + 32)

        # text
        txt = bytes_.decode('utf-8')

        # open file
        with self.output().open("w") as f:
            f.write(txt)

        """
        from clint.textui import progress

        r = requests.get(url, stream=True)
        path = '/some/path/for/file.txt'
        with open(path, 'wb') as f:
            total_length = int(r.headers.get('content-length'))
            for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
                if chunk:
                    f.write(chunk)
                    f.flush()
        """

    def output(self):
        # path
        path = self._filemeta.path
        # target
        target = luigi.LocalTarget(path, format=format.TextFormat)
        return target


def _test_task():
    dt1 = datetime(year=2017, month=3, day=1, hour=0)
    dt2 = datetime.now()

    t1 = DownloadTask(dt1)
    print('t1 created')

    t2 = DownloadTask(dt2)
    print('t2 created')

    t1.run()
    print('t1 over')

    # t2.run()
    print('t2 over')


# tests
def _test_funcs():
    import time

    print('testing...')
    dt = datetime(year=2017, month=3, day=1, hour=0)
    dir = env.temp_abs_path

    print('first call')
    print('list dir = ', os.listdir(dir))
    start_time = time.time()
    download_pageviews(dt)
    print("--- %s seconds ---" % (time.time() - start_time))

    print('second call')
    print('list dir = ', os.listdir(dir))
    start_time = time.time()
    download_pageviews(dt)
    print("--- %s seconds ---" % (time.time() - start_time))

    print('deleting')
    delete_temp(dt)
    print('list dir = ', os.listdir(dir))


# test
if __name__ == '__main__':
    # _test_funcs()
    _test_task()
    pass
