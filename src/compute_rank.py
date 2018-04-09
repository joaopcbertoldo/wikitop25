import gzip
from typing import List, Dict
from datetime import datetime
from tqdm import tqdm

from src.black_list import loader as bl
from src.download import download_pageviews
from src.rank import Rank
from src.configs import Defaults as defaults


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
    black_list = bl.load()

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


if __name__ == '__main__':

    dt = datetime(year=2017, month=3, day=1, hour=0)
    #c = extract_content(dt)

