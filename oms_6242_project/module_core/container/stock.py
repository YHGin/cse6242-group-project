import pandas as pd
from module_core.container.status import Trade
from typing import Optional, Union, Dict, List
import numpy as np

class Stock():

    def __init__(self, ric: str, position: int, price: float, trade_date: pd.Timestamp):
        self.__ric = ric
        self.__position = position
        self.__pnl = 0.0
        self.__side = None
        self.__trade_records = self.__init_trade_record(position_as_of=position, price=price, trade_date=trade_date)

    @property
    def ric(self) -> str:
        return self.__ric

    def trade_records(self) -> List[Trade]:
        return self.__trade_records

    @property
    def position(self) -> int:
        return self.__position

    @property
    def side(self) -> Union[int, None]:
        return self.__side

    @property
    def pnl(self) -> float:
        raise NotImplemented

    def update_trade(self, price: float, trade_date: pd.Timestamp) -> None:
        """

        :param price:
        :param trade_date:
        :return:
        """
        ric = self.__ric
        trade_records = self.__trade_records
        position = self.__position
        status = Trade(ric=ric, new_trade_qty=0, price=price, trade_date=trade_date, position=position)
        trade_records.append(status)
        self.__trade_records = trade_records

    def generate_pnl_ts(self) -> pd.DataFrame:
        """

        :return:
        """
        ric = self.__ric
        trade_records = self.__trade_records
        num_records = len(trade_records)
        t0_trade = trade_records[0]
        data = {"pnl_pct": [0.0],
                "pnl_amt": [0.0],
                "price": [t0_trade.price]}
        df_all_pnl = pd.DataFrame(data=data,
                                  index=[t0_trade.date])
        for i in range(num_records):
            if i + 1 >= num_records:
                break
            else:
                prev_record = trade_records[i]
                new_record = trade_records[i + 1]
                pnl_pct = (new_record.price - prev_record.price) / prev_record.price
                pnl_amt = (new_record.price - prev_record.price) * prev_record.position
                data = {"pnl_pct": [pnl_pct], "pnl_amt": [pnl_amt], "price": [new_record.price]}
                df_pnl = pd.DataFrame(data=data,
                                      index=[new_record.date])
                df_all_pnl = pd.concat([df_all_pnl, df_pnl], axis=0)
        df_all_pnl["ric"] = ric
        return df_all_pnl

    def new_trade(self, qty: int, price: float, trade_date: pd.Timestamp) -> None:
        """

        :param qty:
        :param price:
        :param trade_date:
        :return:
        """
        position = self.__position
        ric = self.__ric
        trade_records = self.__trade_records
        position += qty
        self.__position = position
        status = Trade(ric=ric, new_trade_qty=qty, price=price, trade_date=trade_date, position=position)
        trade_records.append(status)
        self.__trade_records = trade_records

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


def run_stock_test(ric: str = "00001.HK") -> pd.DataFrame:
    trade_date = pd.Timestamp('2023-10-01')
    stock = Stock(ric=ric, position=100, price=50.0, trade_date=trade_date)
    prices = [50 + i * np.random.normal(0,1,1)[0] for i in range(1, 10)]
    for price in prices:
        trade_date = trade_date + pd.Timedelta(days=1)
        stock.update_trade(trade_date=trade_date, price=price)
    df_pnl = stock.generate_pnl_ts()
    return df_pnl


if __name__ == '__main__':
    df = run_stock_test()
    print(df.head(5))