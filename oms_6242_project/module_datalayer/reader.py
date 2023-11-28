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
                      "open": "float",
                      "high": "float",
                      "low": "float",
                      "close": "float",
                      "volume": "float"}


class DbReader(Db):

    def __init__(self, path: str):
        super().__init__(path)

    def get_stock_price(self,
                        rics: List[str],
                        start_date: str,
                        end_date: str) -> Dict[
        str, pd.DataFrame]:
        df_raw = self.fetch_sql(rics, start_date, end_date,table_name="stock_price")
        df_result = self._preprocess(df=df_raw)
        result = self._postprocess(df_result)
        return result

    def get_index_price(self,
                        rics: List[str],
                        start_date: str,
                        end_date: str) -> Dict[
        str, pd.DataFrame]:
        df_raw = self.fetch_sql(rics, start_date, end_date,table_name="index_price")
        df_raw["volume"] = [i.replace("B","") for i in df_raw["volume"]]
        df_result = self._preprocess(df=df_raw)
        result = self._postprocess(df_result)
        return result

    def fetch_sql(self, rics: List[str], start_date: str, end_date: str,table_name:str) -> pd.DataFrame:
        """

        :param rics:
        :param start_date:
        :param end_date:
        :return:
        """
        connection = self._connection
        connection.text_factory = str
        ris_query = str(rics).replace("[", "").replace("]", "")
        ris_query = f"({ris_query})"
        start_date_query = f"date('{start_date}')"
        end_date_query = f"date('{end_date}')"
        sql = f"SELECT * FROM {table_name} where ric in {ris_query} and date >= {start_date_query} and date <= {end_date_query}"
        cursor = connection.execute(sql)
        cols = list(map(lambda x: x[0], cursor.description))
        data = cursor.fetchall()
        df = pd.DataFrame(data=data, columns=cols)
        return df

    def _preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        this private function convert raw mock data object into specific type
        :param df
        :return: pd.DataFrame's data type:
                     Date（Index) -> pd.Timestamp,
                     Open -> float,
                     High -> float,
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

    def _postprocess(self, df: pd.DataFrame):
        data_bag = {}
        for ric, (df_single) in df.groupby(["ric"]):
            data_bag[ric] = df_single
        return data_bag


def db_read_test():
    rics = ["00001.HK"]
    start_date = "2020-06-01"
    end_date = "2023-06-02"
    db_reader = DbReader(path="./resource/db/backtest_db")
    df = db_reader.get_stock_price(rics=rics, start_date=start_date, end_date=end_date)
    print(df.head(2))


def get_dbreader(path) -> DbReader:
    db_reader = DbReader(path=path)
    return db_reader


if __name__ == '__main__':
    db_read_test()
