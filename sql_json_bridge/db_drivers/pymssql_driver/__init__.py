

import pymssql

from sql_json_bridge.db_drivers.base import DatabaseDriver


class MSSQLDriver(DatabaseDriver):
    """
    Driver for accessing MS-SQL Databases using sql_json_bridge.

    This driver requires the freetds binary and the pymssql python package.

    This driver should be instantiated with the following minimum arguments:
        - server:   The server to which to connect.
        - user:     The user with which to connect. If you are using windows
                    authentication, this should include the domain. e.g.,
                    "DOMAIN\\User"
        - password: The password to use to connect.
    Common Optional Arguments:
        - database: The database to which to connect. If not specified,
                    SQL Server will typically choose the default database
                    for the connecting user.
        - port:     The port to which to connect. If not specified,
                    The connection will default to 1443. Note: This
                    can also be specified as part of the host string.

    Additional possible arguments can be found in the _mssql documentation:

    http://pymssql.org/en/stable/ref/pymssql.html#pymssql.connect
    """

    def __init__(self, database_config):
        """
        Initialize this driver using connection information.

        :param args: args to be passed to the connect method.
        :param kwargs: kwargs to be passed to the connect method.
        """
        self.config = database_config

    def connect(self, *args, **kwargs):
        """Connect method is not implemented in this driver."""
        pass

    def run_query(self, query_string):
        """
        Run a query against an MS-SQL database.

        This method will run arbitrary queries against an MS-SQL
        database using this driver.

        :param query_string: query to be run.
        :param type: str
        :returns: The results of the query.
        :rtype: list(dict:?)
        """
        with pymssql.connect(**self.config["connection"]) as conn:
            with conn.cursor(as_dict=True) as cursor:
                cursor.execute(query_string)
                return [row for row in cursor]

    def run_stored_proc(self, proc_name, *variables):
        """
        Run a stored procedure against an MS-SQL database.

        This method will run stored procedures agains an MS-SQL
        database using this driver.

        :param stored_proc: The name of the stored procedure to be run.
        :param type: str
        :param variables: variables to be passed to the stored procedure.
        :returns: The results of the query.
        :rtype: list(dict:?)
        """
        with pymssql.connect(**self.connection_dict) as conn:
            with conn.cursor(as_dict=True) as cursor:
                cursor.callproc(proc_name, variables)
                return [row for row in cursor]
