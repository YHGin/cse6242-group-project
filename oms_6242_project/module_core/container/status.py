import pandas as pd


class Status():

    def __init__(self,
                 ric: str,
                 daily_pnl: float,
                 accumulate_pnl: float,
                 price_change: float,
                 date: pd.Timestamp,
                 notional: float):
        self.__date = date
        self.__ric = ric
        self.__daily_pnl = daily_pnl
        self.__accumulate_pnl = accumulate_pnl
        self.__price_change = price_change
        self.__notional = notional

    @property
    def ric(self) -> str:
        return self.__ric

    @property
    def daily_pnl(self) -> float:
        return self.__daily_pnl

    @property
    def accumulate_pnl(self) -> float:
        return self.__accumulate_pnl

    @property
    def price_change(self) -> float:
        return self.__price_change

    @property
    def date(self) -> pd.Timestamp:
        return self.__date

    @property
    def notional(self) -> float:
        return self.__notional
