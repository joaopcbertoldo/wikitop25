from datetime import datetime

from src.configs import Defaults as defaults
from src.configs import Templates as tmpl


def create_url(dt: datetime) -> str:
    """Create the wikipedia url to download the pageviews for the given datetime."""
    template = tmpl.pageviews_url
    url = dt.strftime(template)
    return url

dt = datetime(year=2017, month=3, day=1, hour=0)


