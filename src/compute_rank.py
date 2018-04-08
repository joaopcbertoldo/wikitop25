from datetime import datetime
from src.download import download_pageviews

dt = datetime(year=2017, month=3, day=1, hour=0)
fpath = download_pageviews(dt)

