# -*- coding: utf-8 -*-
"""
BlackList.py
    Defines the BlackList class, that hides the black list implementation, giving only functions to
    tell if a page is black listed or not.
    Defines a method to load the black list (and "caches" it as an object in a pickle file to avoid reading the txt).
"""

import os
import pickle
from typing import Dict, List

from src.configs import Environment as env


def _load() -> Dict[str, List[str]]:
    """
    Return a dict with per-domain lists of pages (key = domain, value = list of pages).
    If it already exists in a pickle file, loads it from there.
    Otherwise, read the original txt, create the dict and save it in a pickle file.
    """

    # check if the pickle file exists
    exists = os.path.isfile(env.black_list_pickle_path)

    # if yes, load it
    if exists:
        # load the dictionary of page lists from a pickle
        with open(env.black_list_pickle_path, 'rb') as f:
            black_list_dict = pickle.load(f)

    # otherwise, create it
    else:
        # check if the original file with the black list (txt) exists
        assert os.path.isfile(env.black_list_original_path), \
            f"The file '{env.black_list_original_name}' should be put in the folder '{env.black_list_folder}'."

        # read all lines from the black list file
        with open(env.black_list_original_path, encoding='utf-8') as f:
            lines = f.readlines()

        # dict with lists of pages per domain (key = domain, value = list of pages)
        black_list_dict = {}

        for l in lines:
            # split the line's values
            splited = l.split()

            # if it doesn't have at least two items, the whole domain is considered black listed
            if len(splited) < 2:
                splited.append(None)  # None is for the whole domain

            # get domain/page
            domain = splited[0]
            page = splited[1]

            # create a list for the domain if it doesn't exist yet
            if domain not in black_list_dict:
                black_list_dict[domain] = []

            # append the page in the domain's list
            black_list_dict[domain].append(page)

        # dump the dictionary in a pickle file
        with open(env.black_list_pickle_path, 'wb') as f:
            pickle.dump(black_list_dict, f)

    # return the dictionary
    return black_list_dict


# BlackList
class BlackList(object):
    """
    Black list object.
    Useful to hide the black list implementation, giving only functions to tell if a page is black listed or not.
    """

    # init
    def __init__(self):
        # _load it
        self._dic = _load()

    # doesnt_have
    def doesnt_have(self, domain, page):
        """Opposite of has (cf. BlackList.has())."""
        return not self.has(domain, page)

    # has
    def has(self, domain, page) -> bool:
        """Tell whether the black list has a certain page in a given domain."""

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
    # get a playlist
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


# test purposes...
if __name__ == '__main__':
    # _load()
    _test()
