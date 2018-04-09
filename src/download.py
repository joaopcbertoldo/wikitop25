import os
import requests
from datetime import datetime

from src.configs import Templates as tmpl
from src.configs import Environment as env


def create_url(dt: datetime) -> str:
    """Create the wikipedia url to download the pageviews for the given datetime."""

    # get the template
    template = tmpl.pageviews_url

    # replace values
    url = dt.strftime(template)

    # ret
    return url


class DownloadTempFileMeta:

    def __init__(self, dt: datetime):
        self.dt: datetime = dt
        self.url: str = create_url(self.dt)
        self.name: str = self.url.split("/")[-1]
        self.path: str = env.temp_abs_path + self.name

    @property
    def exists(self) -> bool:
        exists = os.path.isfile(self.path)
        return exists


def download_pageviews_job(url: str, file_path: str):
    # open file
    with open(file_path, "wb") as f:

        # get the info from internet
        r = requests.get(url)

        # write it in the file
        f.write(r.content)


def download_pageviews(meta: DownloadTempFileMeta):
    """..."""

    if meta.exists:
        pass
    else:
        download_pageviews_job(meta.url, meta.path)


def delete_job(file_path: str):
    os.remove(file_path)


def delete_temp(meta: DownloadTempFileMeta):
    """..."""
    if meta.exists:
        delete_job(meta.path)
    else:
        pass


# tests
def _tests():
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
    # _tests()