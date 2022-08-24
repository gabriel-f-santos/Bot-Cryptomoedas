import sqlite3 as sql

class DBConnectionHandler:
    """ Sqlalchemy database connection """

    def __init__(self):
        self.cursor = None

    def __enter__(self):
        conn = self.get_engine()
        self.cursor = conn.cursor()
        return conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()

    def get_engine(self):
        """
        :return - engine connection to Database
        """
        conn = sql.connect('Trader.db')
        return conn

