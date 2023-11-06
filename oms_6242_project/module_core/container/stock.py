import pandas as pd
from module_core.container.trade import Trade
from module_core.container.status import Status
from typing import Optional, Union, Dict, List

class Stock():

    def __init__(self, ric: str, position: int, price: float, trade_date: pd.Timestamp):
        self.__ric = ric
        self.__position = position
        self.__pnl = 0.0
        self.__notional = price * position
        self.__trades = self.__init_trade_record(position_as_of=position, price=price, trade_date=trade_date)
        self.__status = self.__init_status_record(trade_date=trade_date)

    @property
    def ric(self) -> str:
        return self.__ric

    @property
    def trades(self) -> List[Trade]:
        return self.__trades

    @property
    def status(self) -> List[Status]:
        return self.__status

    @property
    def position(self) -> int:
        return self.__position

    @property
    def pnl(self) -> float:
        return self.__pnl

    def update_trade(self, current_last: float, trade_date: pd.Timestamp, trade_qty: Optional[int] = 0) -> None:
        """

        :param price:
        :param trade_date:
        :return:
        """
        ric = self.__ric
        trades = self.__trades
        status = self.__status
        prev_position = self.__position
        new_position = self.__position + trade_qty

        last_trade = trades[-1]
        previous_last = last_trade.price
        last_status = status[-1]
        price_change = current_last / previous_last
        notional = (prev_position + trade_qty) * current_last
        daily_pnl = prev_position * (current_last - previous_last)
        accumulate_pnl = last_status.accumulate_pnl + daily_pnl
        current_status = Status(
            date=trade_date,
            ric=ric,
            daily_pnl=daily_pnl,
            notional=notional,
            accumulate_pnl=accumulate_pnl,
            price_change=price_change,
        )
        trade = Trade(ric=ric,
                      new_trade_qty=trade_qty,
                      price=current_last,
                      trade_date=trade_date,
                      position=new_position)
        trades.append(trade)
        status.append(current_status)

        self.__position += trade_qty
        self.__trades = trades
        self.__status = status

    def new_trade(self, qty: int, price: float, trade_date: pd.Timestamp) -> None:
        """

        :param qty:
        :param price:
        :param trade_date:
        :return:
        """
        position = self.__position
        ric = self.__ric
        trades = self.__trades
        position += qty
        self.__position = position
        status = Trade(ric=ric, new_trade_qty=qty, price=price, trade_date=trade_date, position=position)
        trades.append(status)
        self.__trades = trades

    def __init_trade_record(self, position_as_of: int, price: float, trade_date: pd.Timestamp) -> List[Trade]:
        """

        :param position:
        :param price:
        :param trade_date:
        :return:
        """
        ric = self.__ric
        trade = Trade(ric=ric, new_trade_qty=0, position=position_as_of, price=price, trade_date=trade_date)
        trade_records = []
        trade_records.append(trade)
        return trade_records

    def __init_status_record(self, trade_date: pd.Timestamp) -> List[Status]:
        """

        :param position:
        :param price:
        :param trade_date:
        :return:
        """
        ric = self.__ric
        status = Status(ric=ric, notional=0, price_change=0, daily_pnl=0, date=trade_date, accumulate_pnl=0)
        status_record = []
        status_record.append(status)
        return status_record
