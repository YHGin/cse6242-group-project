import pandas as pd
import numpy as np
from abc import ABC
from typing import List
from module_core.container.portfolio import Portfolio
from module_core.container.BackTestInfo import NotionalInfo, PerformanceInfo, SqlTable
from module_datalayer.reader import get_dbreader, DbReader

DB_PATH = "../module_datalayer/resource/db/backtest_db"


class BTCore(ABC):

    def __init__(self, start_date: str, end_date: str, benchmark_ric: str = ".HSI", path: str = DB_PATH):
        self.strategy_pnl = pd.Series()
        self.strategy_status = pd.DataFrame()
        self.benchmark_pnl = pd.Series()
        self.portfolio = Portfolio(start_date=start_date)
        self.initial_portfolio = pd.DataFrame()
        self.benmark_ric = benchmark_ric
        self.start_date = start_date
        self.end_date = end_date
        self._db_reader = get_dbreader(path)

    def get_portfolio_pnl(self) -> pd.DataFrame:
        """
        This function get portfolio performance
        :return:
        """
        field = NotionalInfo.Notional.value
        portfolio = self.portfolio
        all_pnl = []
        for ric in portfolio.stocks.keys():
            stock_attri = self.get_stock_metric(ric=ric, field=field)
            all_pnl.append(stock_attri)
        df_result = pd.concat(all_pnl, axis=1)
        df_result["total_return"] = df_result.sum(axis=1)
        initial_notional = self.initial_portfolio["notional"].sum()
        df_result = df_result["total_return"] / initial_notional
        df_result = df_result.to_frame()
        df_result["ric"] = "portfolio"
        df_result.drop(index=df_result.index[0], axis=0, inplace=True)
        return df_result[["ric","total_return"]]

    def get_stock_pnl(self) -> pd.DataFrame:
        """
        This function get portfolio performance
        :return:
        """
        field = NotionalInfo.Notional.value
        portfolio = self.portfolio
        all_pnl = []
        for ric in portfolio.stocks.keys():
            stock_attri = self.get_stock_metric(ric=ric, field=field)
            all_pnl.append(stock_attri)
        df_result = pd.concat(all_pnl, axis=1)
        for stock in self.initial_portfolio["ric"].drop_duplicates():
            t0_stock = self.initial_portfolio.loc[self.initial_portfolio["ric"] == stock]
            t0_stock_notional = t0_stock["notional"].to_list()[0]
            df_result[stock] = df_result[stock] / t0_stock_notional
        df_result.drop(index=df_result.index[0], axis=0, inplace=True)
        return df_result

    def get_stock_metric(self, ric: str, field: str = "pnl") -> pd.Series:
        """
        This function get individual stock performance
        :param ric:
        :param field:
        :return:
        """
        portfolio = self.portfolio
        stock = portfolio.stocks.get(ric)
        all_status = stock.status
        output = []
        dates = []
        for status in all_status:
            field_attribute = getattr(status, field)
            date = getattr(status, "date")
            dates.append(date)
            output.append(field_attribute)
        pd_output = pd.Series(data=output)
        pd_output.name = ric
        pd_output.index = dates
        return pd_output

    def get_benchmark_pnl(self) -> pd.DataFrame:
        db_reader = self._db_reader
        benchmark_ric = self.benmark_ric
        start_date = self.start_date
        end_date = self.end_date
        price = db_reader.get_index_price(rics=[benchmark_ric], start_date=start_date, end_date=end_date)
        price = price[self.benmark_ric]
        price["total_return"] = price["close"] / price["close"][0]
        df_benmark_pnl = price.copy()
        df_benmark_pnl = df_benmark_pnl[["ric", "total_return"]]
        df_benmark_pnl.drop(index=df_benmark_pnl.index[0], axis=0, inplace=True)
        return df_benmark_pnl[["ric","total_return"]]

    def get_vol_status(self) -> pd.Series:
        raise NotImplemented

    def get_t0_port_notional(self, df_sod_price: pd.DataFrame, df_portfolio: pd.DataFrame) -> pd.DataFrame():
        t0_portfolio = pd.merge(left=df_portfolio, right=df_sod_price, on=["ric"])
        t0_portfolio["notional"] = t0_portfolio["qty"] * t0_portfolio["open"]
        return t0_portfolio
