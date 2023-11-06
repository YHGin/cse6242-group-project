import pandas as pd
import numpy as np
from abc import ABC
from typing import List
from container.portfolio import Portfolio
from module_core.container.BackTestInfo import NotionalInfo, PerformanceInfo


class BTCore(ABC):

    def __init__(self, start_date: str, benchmark_ric: str = ".HSI"):
        self.strategy_pnl = pd.Series()
        self.strategy_status = pd.DataFrame()
        self.benchmark_pnl = pd.Series()
        self.portfolio = Portfolio(start_date=start_date)

    def get_portfolio_metric(self, field: str) -> pd.DataFrame:
        """
        This function get portfolio performance
        :return:
        """
        portfolio = self.portfolio
        all_pnl = []
        for ric in portfolio.stocks.keys():
            stock_pnl = self.get_stock_metric(ric=ric, field=field)
            all_pnl.append(stock_pnl)
        df_result = pd.concat(all_pnl, axis=1)
        if field in [e.value for e in NotionalInfo]:
            df_result["total_return"] = df_result.sum(axis=1)
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

    def get_benchmark_pnl(self) -> pd.Series:
        raise NotImplemented
