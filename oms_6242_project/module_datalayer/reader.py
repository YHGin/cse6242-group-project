"""
This utility.sample.script is the SQLite query function
1. stock historical price reader
    a.query parser
    b.preprocess
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Union, Tuple
from module_datalayer.db import Db

HISTORICAL_COLUMNS = {"date": "datetime64[ns]",
                      "ric": np.dtype('O'),
                      "high": "float",
                      "low": "float",
                      "close": "float",
                      "volume": "int"}


class DbReader(Db):

    def __init__(self, path: str):
        super().__init__(path)

    def get_stock_price(self, rics: List[str], start_date: pd.Timestamp, end_date: pd.Timestamp) -> pd.DataFrame:
        df_raw = self.fetch_sql(rics, start_date, end_date)
        df_result = self.preprocess(df=df_raw)
        return df_result

    def fetch_sql(self, rics: List[str], start_date: pd.Timestamp, end_date: pd.Timestamp) -> pd.DataFrame:
        """

        :param rics:
        :param start_date:
        :param end_date:
        :return:
        """
        connection = self._connection
        connection.text_factory = str
        ric_query = ""
        for ric in rics:
            ric_str = f"\"{ric}\""
            ric_query += ric_str
            ric_query += ",\"\""
        sql = f"SELECT * FROM stock_price where ric IN ({ric_query})"
        cursor = connection.execute(sql)
        cols = list(map(lambda x: x[0], cursor.description))
        data = cursor.fetchall()
        df = pd.DataFrame(data=data, columns=cols)
        return df

    def preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        this private function convert raw mock data object into specific type
        :param df
        :return: pd.DataFrame's data type:
                     Date（Index) -> pd.Timestamp,
                     High -> pfloat,
                     Low -> float,
                     Close -> float,
                     Volume -> int
        """
        cols = set(HISTORICAL_COLUMNS.keys())
        if not set(df.columns) == cols:
            raise ValueError(f"Expect _preprocess df container:{cols}")
        df = df.astype(HISTORICAL_COLUMNS)
        df = df.set_index("date")
        return df


def db_read_test():
    rics = ["00001.HK", "00002.HK"]
    start_date = pd.Timestamp("2004-01-01")
    end_date = pd.Timestamp("2010-01-01")
    db_reader = DbReader(path="./resource/db/backtest_db")
    df = db_reader.get_stock_price(rics, start_date, end_date)
    print(df.head(2))

if __name__ == '__main__':
    db_read_test()
