# src/agrovision/utils/file_utils.py
import os


def create_dir_if_not_exists(path: str):
    """Creates a directory if it does not exist."""
    if not os.path.exists(path):
        os.makedirs(path)
