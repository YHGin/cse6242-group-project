from enum import Enum


class NotionalInfo(Enum):
    DailyPnl = "daily_pnl"
    Notional = "notional"
    AccumulatePnl = "accumulate_pnl"


class PerformanceInfo(Enum):
    PriceChange = "price_change"


class SqlTable(Enum):
    stock_price = "stock_price"
    index_price = "index_price"