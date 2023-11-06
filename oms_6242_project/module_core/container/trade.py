import pandas as pd
from module_core.container.side import TradeType
from typing import Optional, Union


class Trade():

    def __init__(self, ric: str, position: int, new_trade_qty: int, price: float, trade_date: pd.Timestamp):
        self.__ric = ric
        self.__new_trade_qty = new_trade_qty
        self.__position = position
        self.__price = price
        self.__date = trade_date
        self.__side = self.generate_side(new_trade_qty)

    def generate_side(self, qty: int):
        if qty > 0:
            return TradeType.Buy
        elif qty < 0:
            return TradeType.Sell
        elif qty == 0:
            return TradeType.Hold

    @property
    def ric(self) -> str:
        return self.__ric

    @property
    def qty(self) -> int:
        return self.__new_trade_qty

    @property
    def price(self) -> float:
        return self.__price

    @property
    def date(self) -> pd.Timestamp:
        return self.__date

    @property
    def side(self) -> TradeType:
        return self.__side

    @property
    def position(self) -> int:
        return self.__position
