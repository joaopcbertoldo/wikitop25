import os

from src.configs import Environment as env


def _ensure_folder(abs_path):
    # check existence
    exists = os.path.isdir(abs_path)

    # create if it doesnt exist
    if not exists:
        os.makedirs(abs_path)


def setup_temp():
    # temp folder
    _ensure_folder(env.temp_abs_path)

    # temp download folder
    _ensure_folder(env.temp_download_abs_path)
