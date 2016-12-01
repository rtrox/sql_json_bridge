"""Keyring Access for SQL-HTTP-Bridge."""
# Copyright (C) 2016 Russell Troxel

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import re

from db_drivers import load_db_driver

import yaml


def load_database_configs(directory):
    databases = {}
    for (dirpath, dirnames, filenames) in os.walk(directory):
        for f in filenames:
            if f.endswith(('.yml', '.yaml')):
                conf = DbConfig(os.path.join(dirpath, f))
                databases[conf['identifier']] = conf


class DbConfig(object):
    """
    DbConfig object to represent the configuration of a specific database.

    This object will represent a single database group from the configuration
    file and will populate all variables into configuration options and
    dictionaries automatically.
    """

    def __init__(self, config_file):
        self.store = dict()
        with open(config_file, "r") as f:
            self.store.update(
                yaml.load(f.read())
            )
        self.store["identifier"] = re.compile(self.store["identifier"])
        self.driver = load_db_driver(self.store["driver"], self)

    def populate_args(self, obj, args):
        """
        Populate args into item.

        Arguments for replacement in string will use basic jinja
        style format: '{{0}}', '{{1}}', etc. these will be replaced
        with the corresponding list item:
        {{0}} = args[0], etc.

        Replacement will be done recursively if given a dict.

        :param string string: string to be populated.
        :param list args: list of arguments for population.
        :rtype string:
        """
        if isinstance(obj, str):
            to_replace = obj.finditer(r'{{([0-9]+)}}')
            for i in to_replace:
                key = int(re.search(r'\d+', i).group())
                obj.replace(i, args[key])

        elif isinstance(obj, dict):
            for k, v in obj.items:
                obj[k] = self.populate_args(v)

        return obj


    def get_item(self, database_name, key):
        """
        Get item from config store with args replaced based on identifier.
        "{{\d}}" will be replaced with the corresponding zero-indexed regex
        group (regex group 1 becomes 0, etc).
        """
        args = self["identifier"].match(database_name).groups()
        return self.populate_args(self.store[key], args)
