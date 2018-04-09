# -*- coding: utf-8 -*-
"""
Setups necessary stuff in the application environment (as the temp folders).
Module called uniquely by the main.
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
def setup_temp():
    """Setup the temp folder and it's subfolders (this means that it ensures their existences)."""

    # temp folder
    _ensure_folder(env.temp_abs_path)

    # temp download folder
    _ensure_folder(env.temp_download_abs_path)

    # temp rank pickle
    _ensure_folder(env.temp_rank_pickle_abs_path)
