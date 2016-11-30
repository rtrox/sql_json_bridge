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

from functools import wraps

from stevedore import driver


def load_authenticator(driver_name, configuration_details):
    """
    Load an instance of a database driver.

    These drivers should exist in the "sql_json_bridge.ext.database_driver"
    namespace, and should have short, readable names. For example, "mssql",
    "sqlalchemy", or "mysql_safemode".

    :param driver_name: The name of the driver to be loaded.
    :type driver_name: str
    :param connection_details: Connection details to be used for the
                               database. These vary on a driver by driver
                               basis.
    :type connection_details:  dict
    :returns: A database object.
    :rtype: :py:class:base.DatabaseDriver
    """
    mgr = driver.DriverManager(
        namespace="sql_json_bridge.ext.database_driver",
        name=driver_name,
        invoke_on_load=True,
        invoke_args=(configuration_details),
    )
    return mgr.driver


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        pass
        return f(*args, **kwargs)
    return decorated
