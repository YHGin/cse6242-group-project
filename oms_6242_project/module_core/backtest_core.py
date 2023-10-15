import pandas as pd
import numpy as np
from abc import ABC
from typing import List

class BackTestCore(ABC):

    def __int__(self):
        self.strategy_pnl = pd.Series()
        self.strategy_status = pd.DataFrame()
        self.benchmark_pnl = pd.Series()

    def strategy_status(self)-> pd.DataFrame:
        raise NotImplemented

    def get_strategy_pnl(self)-> pd.Series:
        raise NotImplemented

    def get_benchmark_pnl(self)-> pd.Series:
        raise NotImplemented
