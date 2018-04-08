import os.path
import pickle
from typing import Dict

from src.configs import Environment as env


def load() -> Dict[str, str]:

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


if __name__ == '__main__':
    load()
