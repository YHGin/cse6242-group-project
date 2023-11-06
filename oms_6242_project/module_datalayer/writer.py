"""
This utility.sample.script is the SQLite write function
1. stock historical price writer
schema
"""

import sqlite3
from sqlite3 import Error
import pandas as pd
from module_datalayer.db import Db
import os

class DbWriter(Db):

    def __init__(self, path: str):
        super().__init__(path)

    def write_csv_data(self, table_name: str, df: pd.DataFrame, ric: str):
        """

        :param table_name: sql table name
        :param df: pandas data content
        :return: None
        """
        connection = self._connection
        connection.text_factory = str
        cursor = connection.cursor()
        for index, (date, open, high, low, close, volume) in df.iterrows():
            try:
                sql_content = (date, ric, open, high, low, close, volume)
                sql_insert_row = f"INSERT INTO {table_name} VALUES (?,?,?,?,?,?,?)"
                cursor.execute(sql_insert_row, sql_content)
            except Exception as e:
                print(f'fail to execute write error: {e}')
        connection.commit()


def writer_test():
    df_hk00001 = pd.read_csv("./resource/mock_data/00001HK.csv")
    df_hk00002 = pd.read_csv("./resource/mock_data/00002HK.csv")
    df_hsi = pd.read_csv("./resource/mock_data/HSI.csv")
    db = DbWriter(path="./resource/db/backtest_db")
    db.write_csv_data(table_name="stock_price", df=df_hk00001, ric="00001.HK")
    db.write_csv_data(table_name="stock_price", df=df_hk00002, ric="00002.HK")
    db.write_csv_data(table_name="index_price", df=df_hsi, ric=".HSI")

def bulk_writter():
    directory = f'./resource/real_data/price/'
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            df = pd.read_csv(f)
            db = DbWriter(path="./resource/db/backtest_db")
            file_name = f.split("/")[-1]
            if file_name == "hsi.csv":
                db.write_csv_data(table_name="index_price", df=df, ric=".HSI")
            else:
                ric = file_name.replace(".csv",".HK")
                db.write_csv_data(table_name="stock_price", df=df, ric=ric)

if __name__ == '__main__':
    bulk_writter()
