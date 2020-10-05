import os


def check_dir(dirname):
    os.makedirs(os.path.abspath(dirname), exist_ok=True)
