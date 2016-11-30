"""Main View for Database queries and listing."""
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>

import abc

import six


@six.add_metaclass(abc.ABCMeta)
class DatabaseDriver(object):
    """
    Modular stevedore Driver MetaClass for accessing databases.

    Should be installed with a "sql_json_bridge.ext.database_driver"
    entrypoint.
    """

    def __init__(self, database_config):
        self.config = database_config

    @abc.abstractmethod
    def connect(self, *args, **kwargs):
        """
        Connect to the database represented by this driver.

        If no connection method is needed, override this method with `pass`.
        This function should attach a connection object to the database
        object if one is necessary.

        :param *args: Arguments to be passed to the connection method
                      of your underlying lybrary.
        :type *args: list
        :param **kwargs: Keyword Arguments to be passed to the connection
                         method o
        :type **kwargs: list
        """
        raise NotImplementedError

    @abc.abstractmethod
    def run_query(self, query_string):
        """
        Run a Query against the database represented by the driver.

        :param query_string: Query to be ran against the database.
        :type query_string: str
        :returns: An iterable cursor of results.
        """
        raise NotImplementedError

    def run_update(self, query_string):
        """
        Run an update function against a database.

        By default, this function is an alias to run_query. If separate
        code is needed by your driver to perform an update, you can
        override this behavior here.

        :param query_string: Query to be ran against the database.
        :type query_string: str
        :returns: An iterable cursor of results.
        """
        self.run_query(query_string)

    def run_delete(self, query_string):
        """
        Run an update function against a database.

        By default, this function is an alias to run_query. If separate
        code is needed by your driver to perform an update, you can
        override this behavior here.

        :param query_string: Query to be ran against the database.
        :type query_string: str
        :returns: An iterable cursor of results.
        """
        self.run_query(query_string)

    def run_stored_proc(self, proc_name, **variables):
        """
        Run a stored procedure against this database.

        If needed, this method can be used as a helper function to call
        a stored procedure against the database by overriding this function.

        :param proc_name: The name of the stored procedure to be run.
        :type proc_name: str
        :param **kwargs: Keyword pairs for stored procedure variables.
        :returns: An iterable cursor of results.
        """
        raise NotImplementedError
