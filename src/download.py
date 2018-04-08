import os
import requests
from datetime import datetime

from src.configs import Templates as tmpl
from src.configs import Environment as env


temp_exists = os.path.isdir(env.temp_abs_path)

if not temp_exists:
    os.makedirs(env.temp_abs_path)


def create_url(dt: datetime) -> str:
    """Create the wikipedia url to download the pageviews for the given datetime."""
    template = tmpl.pageviews_url
    url = dt.strftime(template)
    return url


class TempFile:

    def __init__(self, dt: datetime):
        self.dt: datetime = dt
        self.url: str = create_url(self.dt)
        self.name: str = self.url.split("/")[-1]
        self.path: str = env.temp_abs_path + self.name

    @property
    def exists(self) -> bool:
        exists = os.path.isfile(self.path)
        return exists


def download_pageviews(dt: datetime):
    """..."""
    tfile = TempFile(dt)

    if tfile.exists:
        pass

    else:
        with open(tfile.path, "wb") as f:
            r = requests.get(tfile.url)
            f.write(r.content)


def delete_temp(dt: datetime):
    """..."""
    tfile = TempFile(dt)

    if tfile.exists:
        os.remove(tfile.path)
    else:
        pass


# test
if __name__ == '__main__':
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
