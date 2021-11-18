import os
from pathlib import Path

import yaml

from pydantic import BaseModel, Field


class Config(BaseModel):
    root: str
    path_to_posts: str
    path_to_static: str
    prefix_img: str = ''

    def path_to_posts_abs(self):
        return Path(self.root, self.path_to_posts)

    def path_to_static_abs(self):
        return Path(self.root, self.path_to_static)


def find_file_recursively(name, max_levels_up=6, starting_dir=None):
    """
    Find a file by looking into the current folder and parent folders,
    returns None if no file was found otherwise pathlib.Path to the file

    Parameters
    ----------
    name : str
        Filename

    Returns
    -------
    path : str
        Absolute path to the file
    levels : int
        How many levels up the file is located
    """
    current_dir = starting_dir or os.getcwd()
    current_dir = Path(current_dir).resolve()
    path_to_file = None
    levels = None

    for levels in range(max_levels_up):
        current_path = Path(current_dir, name)

        if current_path.exists():
            path_to_file = current_path.resolve()
            break

        current_dir = current_dir.parent

    return path_to_file, levels


def get_config():
    """
    Load jupyblog configuration file
    """
    NAME = 'jupyblog.yaml'

    path, _ = find_file_recursively(NAME)

    if path is None:
        raise FileNotFoundError(f'Could not find {NAME}')

    cfg = Config(**yaml.safe_load(Path(path).read_text()),
                 root=str(path.parent))

    if cfg.path_to_posts_abs().is_dir() and cfg.path_to_static_abs().is_dir():
        return cfg
    else:
        raise NotADirectoryError(
            f'missing {cfg.path_to_posts_abs()} or {cfg.path_to_static_abs()}')


def get_local_config():
    Path('output').mkdir()
    return Config(path_to_posts='output',
                  path_to_static='output',
                  prefix_img='',
                  root='.')
