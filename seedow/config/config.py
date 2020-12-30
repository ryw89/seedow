"""Configuration for this package."""

import os
import shutil

import appdirs
import pkg_resources
import toml

from ..lib.py.pkg import get_base_pkg


def get_config(attr):
    config = Config()
    return config.__getattr__(attr)


def get_wikipedia_sleep():
    return float(get_config('wikipedia')['sleep'])


class Config():
    """Fetch configuration for this package using its config.toml file."""
    def __init__(self):
        self.data_dir = appdirs.user_data_dir('seedow', 'seedow')
        self.config_dir = appdirs.user_config_dir('seedow', 'seedow')
        self.config_path = os.path.join(self.config_dir, 'config.toml')

        try:
            self.load_config()
        except FileNotFoundError:
            self.write_default_config()
            self.load_config()

    def __getattr__(self, attr):
        try:
            return self.config[attr]
        except KeyError:
            raise AttributeError

    def load_config(self):
        """Load config.toml."""
        with open(self.config_path) as f:
            self.config = toml.load(f)

    def write_default_config(self):
        """Save this package's default config to the user's config directory."""
        conf = pkg_resources.resource_filename(get_base_pkg(),
                                               'data/config.toml')
        try:
            shutil.copy(conf, self.config_path)
        except IOError:
            try:
                os.makedirs(os.path.dirname(self.config_path))
            except FileExistsError:
                pass

            shutil.copy(conf, self.config_path)
