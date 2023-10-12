from backtesting import Backtest, Strategy
from backtesting.lib import crossover

import numpy as np
import pandas as pd
import pandas_datareader as web
import plotly.express as px
import pandas_datareader
import datetime
import pandas_datareader.data as web
import plotly.graph_objects as go
from backtest_core import BackTestCore


class BuyHoldTest(BackTestCore):

    def __int__(self):
        raise NotImplemented
