import os
import requests
from datetime import datetime

from src.configs import Defaults as defaults
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


def download_pageviews(dt: datetime):
    """..."""
    url = create_url(dt)
    filename = url.split("/")[-1]
    filepath = env.temp_abs_path + filename
    file_exists = os.path.isfile(filepath)

    if file_exists:
        pass
    else:
        with open(filepath, "wb") as f:
            r = requests.get(url)
            f.write(r.content)


# test
if __name__ == '__main__':
    import time
    start_time = time.time()
    dt = datetime(year=2017, month=3, day=1, hour=0)
    download_pageviews(dt)
    print("--- %s seconds ---" % (time.time() - start_time))




