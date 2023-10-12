import pandas as pd
from side import TradeType
from typing import Optional


class Stock():

    def __int__(self, ric: str, position: int, price: float, name: Optional[str] = None):
        self.__ric = ric
        self.__old_position = position
        self.__new_position = position
        self.__old_price = price
        self.__new_price = price
        self.__name = name
        self.__pnl = 0.0

    @property
    def ric(self) -> str:
        raise NotImplemented

    @property
    def name(self) -> str:
        raise NotImplemented

    @property
    def old_position(self) -> int:
        return self.__old_position

    @property
    def new_position(self) -> int:
        return self.__new_position

    @property
    def side(self) -> int:
        raise NotImplemented

    @property
    def pnl(self) -> float:
        raise NotImplemented


    def trade(self, qty: int, side: TradeType) -> None:
        new_position = self.__new_position
        if side == TradeType.Buy:
            new_position += qty
        if side == TradeType.Sell:
            new_position -= qty
