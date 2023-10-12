from abc import ABC
import sqlite3
from sqlite3 import Error
import logging

class Db(ABC):

    def __init__(self, path: str):
        self._connection = self.__create_connection(path=path)

    def __create_connection(self, path) -> sqlite3.Connection:
        """
        :param db path:
        :return:  sqlite3 Db Connection
        """
        connection = None
        try:
            connection = sqlite3.connect(path)
            connection.text_factory = str
            logging.info(f"connect to db sucess")
        except Error as e:
            print("Error occurred: " + str(e))
        return connection
