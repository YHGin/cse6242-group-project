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
        self.benchmark_pnl = pd.DataFrame()
        self.portfolio = Portfolio(start_date=start_date)
        self.initial_portfolio = pd.DataFrame()
        self.benmark_ric = benchmark_ric
        self.start_date = start_date
        self.end_date = end_date
        self._db_reader = get_dbreader(path)
        self.portfolio_pnl = pd.DataFrame()
        self.stock_pnl = pd.DataFrame()
        self.portfolo_states = pd.DataFrame()

    def get_portfolio_pnl(self) -> pd.DataFrame:
        """
        This function get portfolio performance
        :return:
        """

        if not self.portfolio_pnl.empty:
            return self.portfolio_pnl

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
        self.portfolio_pnl = df_result[["ric", "total_return"]]
        return self.portfolio_pnl

    def get_stock_pnl(self) -> pd.DataFrame:
        """
        This function get portfolio performance
        :return:
        """
        if not self.stock_pnl.empty:
            return self.stock_pnl
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
        self.stock_pnl = df_result
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
        if not self.benchmark_pnl.empty:
            return self.benchmark_pnl
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
        df_benmark_pnl = df_benmark_pnl[["ric", "total_return"]]
        self.benchmark_pnl = df_benmark_pnl
        return self.benchmark_pnl

    def get_performance_states(self) -> pd.DataFrame:
        stock_pnl = self.stock_pnl
        portfolio_pnl = self.portfolio_pnl
        benchmark_pnl = self.benchmark_pnl
        start_date = self.start_date
        end_date = self.end_date
        duration = pd.Timestamp(end_date) - pd.Timestamp(start_date)
        vol = portfolio_pnl["total_return"].std()
        returns = portfolio_pnl["total_return"]
        return_peak = (returns.max() - 1)
        equity_total = (returns[-1] - 1)
        return_result = (returns[-1] - 1)
        sharp = (equity_total - 0.03) / (vol * np.sqrt(255))
        portfolio_pnl["total_return_before"] = portfolio_pnl["total_return"].shift(1).fillna(1)
        period_log_return = np.log(portfolio_pnl["total_return"] / portfolio_pnl["total_return_before"])
        sortino_vol = period_log_return.loc[period_log_return < 0].std()
        sortino = equity_total / (sortino_vol * np.sqrt(255))
        max_drawdown = 0 if period_log_return.min() > 0 else period_log_return.min()
        avg_drawdown = period_log_return.loc[period_log_return < 0].mean()
        trades = len(stock_pnl.columns)
        benchmark_pnl = benchmark_pnl["total_return"].iloc[-1] - 1
        stock_rank = stock_pnl.tail(1).max().reset_index().sort_values(by=0)
        best_stock_name = stock_rank.iloc[-1, 0]
        best_stock_return = stock_rank.iloc[-1, 1] - 1
        worst_stock_name = stock_rank.iloc[0, 0]
        worst_stock_return = stock_rank.iloc[0, 1] - 1
        rounder = 2
        data = {'Start': self.start_date,
                'End': self.end_date,
                'Duration': str(duration.days),
                'Return Peak [%]': round(return_peak * 100, rounder),
                'Return [%]': round(return_result * 100, rounder),
                'Return Benchmarket [%]': round(benchmark_pnl * 100, rounder),
                'Volatility (Ann.) [%]': round(vol * 100 * np.sqrt(252), rounder),
                'Sharpe Ratio [%]': round(sharp * 100, rounder),
                'Sortino Ratio(Ann.) [%]': round(sortino * 100, rounder),
                'Max. Daily Drawdown [%]': round(max_drawdown * 100, rounder),
                'Avg. Daily Drawdown [%]': round(avg_drawdown * 100, rounder),
                '# Trades': trades,
                'Best Trade Name': best_stock_name,
                'Best Trade [%]': round(best_stock_return * 100, rounder),
                'Worse Trade Name': worst_stock_name,
                'Worst Trade [%]': round(worst_stock_return * 100, rounder),
                }
        performance_status = pd.Series(data=data)
        df = performance_status.to_frame().reset_index()
        df = df.rename(columns={"index": "param", 0: ""})
        return df

    def get_t0_port_notional(self, df_sod_price: pd.DataFrame, df_portfolio: pd.DataFrame) -> pd.DataFrame():
        t0_portfolio = pd.merge(left=df_portfolio, right=df_sod_price, on=["ric"])
        t0_portfolio["notional"] = t0_portfolio["qty"] * t0_portfolio["open"]
        return t0_portfolio
