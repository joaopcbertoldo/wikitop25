import os.path
import pickle
from typing import Dict

# text filename
tfname = 'blacklist_domains_and_pages'

# pickle filename
pfname = 'black_list_dict.pickle'


def load() -> Dict[str, str]:
    global tfname, pfname

    # check if the pickle exists
    exists = os.path.isfile(pfname)

    if exists:
        # check if the original exists
        assert os.path.isfile(tfname), f"The file '{tfname}' should be put in the folder '{os.path.abspath('.')}'."

        with open(pfname, 'rb') as f:
            black_list_dict = pickle.load(f)

    else:
        with open(tfname, encoding='utf-8') as f:
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

        with open(pfname, 'wb') as f:
            pickle.dump(black_list_dict, f)
    return black_list_dict
