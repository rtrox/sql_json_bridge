

import pymysql.cursors

from sql_json_bridge.db_drivers.base import DatabaseDriver


class MySQLDriver(DatabaseDriver):
    """
    Driver for accessing MYSQL Databases using sql_json_bridge.

    This driver requires pymysql library to be installed.

    This driver should be instantiated with the following minimum arguments
    in it's connection dictionary:
        - host:     The server to which to connect.
        - user:     The user with which to connect.
        - password: The password to use to connect.
        - port:     The port to utilize.
        - db:       The database to connect to.
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
        connection = pymysql.connect(cursorclass=pymysql.cursors.DictCursor,
                                     **self.config["connection"])
        return connection

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
        # try:
        connection = self.connect()
        with connection.cursor() as cur:
            cur.execute(query_string)
            return cur.fetchall()
        # finally:
        connection.close()
