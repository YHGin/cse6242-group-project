from typing import List

import pandas as pd
from typing import Dict
from module_core.container.stock import Stock

class Portfolio():
    def __init__(self, start_date: str):
        self.__stocks = {}
        self.__asof = start_date

    @property
    def stocks(self) -> Dict[str, Stock]:
        return self.__stocks

    @property
    def balance(self) -> pd.DataFrame:
        stocks = self.__stocks
        stock_bag = []
        for stock_name, stock in stocks.items():
            position = stock.position
            pnl = stock.pnl
            ric = stock.ric
            notional = stock.notional
            df = pd.DataFrame(data={"ric": [ric], "position": [position], "notional": [notional], "pnl": [pnl]})
            stock_bag.append(df)
        df_balance = pd.concat(stock_bag, axis=0)
        return df_balance

    @property
    def notional(self) -> float:
        df = self.balance
        return df["notional"].sum()

    @property
    def asof(self) -> str:
        return self.__asof

    def update(self, stock: Stock):
        ric = stock.ric
        self.stocks[ric] = stock
