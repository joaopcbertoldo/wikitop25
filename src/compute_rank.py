import gzip
from typing import List
from datetime import datetime

from src.download import download_pageviews


def _transform(line: bytes) -> List:
    return line.decode('utf-8').split()[0:3]


def extract_content(dt: datetime) -> List:

    fpath = download_pageviews(dt)

    with gzip.open(fpath, 'rb') as f:
        content = [_transform(line) for line in f.readlines()]

    return content


if __name__ == '__main__':

    dt = datetime(year=2017, month=3, day=1, hour=0)
    c = extract_content(dt)

