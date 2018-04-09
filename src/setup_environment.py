import os

from src.configs import Environment as env


def execute():
    temp_exists = os.path.isdir(env.temp_abs_path)

    if not temp_exists:
        os.makedirs(env.temp_abs_path)

