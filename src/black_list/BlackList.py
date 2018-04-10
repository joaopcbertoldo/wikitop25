# -*- coding: utf-8 -*-
"""

"""

import os
import pickle
from typing import Dict, List

from src.configs import Environment as env


def load() -> Dict[str, List[str]]:
    """todo doc load (black list)"""

    # check if the pickle exists
    exists = os.path.isfile(env.black_list_pickle_path)

    if exists:
        with open(env.black_list_pickle_path, 'rb') as f:
            black_list_dict = pickle.load(f)

    else:
        # check if the original exists
        assert os.path.isfile(env.black_list_original_path), \
            f"The file '{env.black_list_original_name}' should be put in the folder '{env.black_list_folder}'."

        with open(env.black_list_original_path, encoding='utf-8') as f:
            lines = f.readlines()

        black_list_dict = {}

        for l in lines:
            splited = l.split()
            if len(splited) < 2:
                splited.append(None)
            domain = splited[0]
            page = splited[1]
            if domain not in black_list_dict:
                black_list_dict[domain] = []
            black_list_dict[domain].append(page)

        with open(env.black_list_pickle_path, 'wb') as f:
            pickle.dump(black_list_dict, f)

    return black_list_dict


# BlackList
class BlackList(object):
    """Black list object."""

    # init
    def __init__(self):
        # load it
        self._dic = load()

    # doesnt_have
    def doesnt_have(self, domain, page):
        return not self.has(domain, page)

    # is in
    def has(self, domain, page) -> bool:

        # get the domain's black list
        domain_bl = self._dic.get(domain, None)

        # if it is none, the domain has no black list
        if domain_bl is None:
            return False

        # if None is in the black list, every page is considered black listed
        if None in domain_bl:
            return True

        # otherwise, check it
        return page in domain_bl


# test
def _test():
    bl = BlackList()

    lines = """
    ace Beureukaih:Nuvola_apps_important.svg
    ace Japan
    af .sy
    af 2009
    af Apostelskap
    """.strip().split('\n')

    # positive cases
    tuples = [tuple(line.split()) for line in lines]

    # negative
    tuples.append(('en', 'fake'))
    tuples.append(('pt', 'brazil is the best'))

    # do the tests
    for domain, page in tuples:
        print(f'domain: {domain}, page: {page}')
        print(bl.has(domain, page))
        print()


# run test
if __name__ == '__main__':
    # load()
    _test()
