# -*- coding: utf-8 -*-
"""
setup_environment.py
    Setups necessary conditions of the application environment (as the temp folders).
"""

import os

from src.configs import Environment as env


# ensure folder
def _ensure_folder(abs_path: str):
    """Ensure that a folder exists in the given absolute path."""

    # check existence
    exists = os.path.isdir(abs_path)

    # create if it doesnt exist
    if not exists:
        os.makedirs(abs_path)


# setup temp
def _setup_folders():
    """Setup the necessary folders and their subfolders (this means that it ensures their existences)."""

    # temp folder
    _ensure_folder(env.temp_abs_path)

    # temp download folder
    _ensure_folder(env.temp_download_abs_path)

    # temp rank pickle
    _ensure_folder(env.temp_rank_pickle_abs_path)

    # ranks folder
    _ensure_folder(env.ranks_abs_path)


def run():
    """
    Run every necessary setup.

    For now there is only one function thing to be called, but, as the application changes, there could be other
    things, so having one only function to be called keeps the main unchanged.
    """

    # folders
    _setup_folders()


# test purposes...
if __name__ == '__main__':
    _setup_folders()
