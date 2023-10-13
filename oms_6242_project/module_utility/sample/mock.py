import pandas as pd
import os


def MOCK_DATA(ric: str) -> pd.DataFrame:
    """
    This is the mocked stock data reading csv file
    :return: pd.Dataframe contains col
                Date,High,Low,Close,Volume
    """
    df = pd.read_csv(f"{ric}.csv")
    return df.dropna()


def MOCK_INDEX_DATA(index_ric: str) -> pd.DataFrame:
    """
    This is the mock data reading  csv file
    :return: pd.Dataframe contains col
                Date,High,Low,Close,Volume
    """
    df = pd.read_csv(f"{index_ric}.csv")
    return df.dropna()


def MOCK_PERFORMANCE_STATUS():
    """
    Start                     2004-08-19 00:00:00
    End                       2013-03-01 00:00:00
    Duration                   3116 days 00:00:00
    Exposure Time [%]                     93.9944
    Equity Final [$]                      51959.9
    Equity Peak [$]                       75787.4
    Return [%]                            419.599
    Buy & Hold Return [%]                 703.458
    Return (Ann.) [%]                      21.328
    Volatility (Ann.) [%]                 36.5383
    Sharpe Ratio                         0.583718
    Sortino Ratio                         1.09239
    Calmar Ratio                         0.444518
    Max. Drawdown [%]                    -47.9801
    Avg. Drawdown [%]                    -5.92585
    Max. Drawdown Duration      584 days 00:00:00
    Avg. Drawdown Duration       41 days 00:00:00
    # Trades                                   65
    Win Rate [%]                          46.1538
    Best Trade [%]                         53.596
    Worst Trade [%]                      -18.3989
    Avg. Trade [%]                        2.35371
    Max. Trade Duration         183 days 00:00:00
    Avg. Trade Duration          46 days 00:00:00
    Profit Factor                         2.08802
    Expectancy [%]                        8.79171
    SQN                                   0.916893
    :return:
    """

    data = {'Start': pd.Timestamp('2023-10-01 00:00:00'),
            'End': pd.Timestamp('2023-10-11 00:00:00'),
            'Duration': str(pd.Timedelta('3116 days 00:00:00')),
            'Exposure Time [%]': 97.06703910614524,
            'Equity Final [$]': 68221.96986000001,
            'Equity Peak [$]': 68991.21986000001,
            'Return [%]': 582.2196986000001,
            'Buy & Hold Return [%]': 703.4582419772772,
            'Return (Ann.) [%]': 25.266426719390832,
            'Volatility (Ann.) [%]': 38.38300814823962,
            'Sharpe Ratio': 0.6582711449245711,
            'Sortino Ratio': 1.2887794382233382,
            'Calmar Ratio': 0.7637475148882401,
            'Max. Drawdown [%]': -33.082172088099156,
            'Avg. Drawdown [%]': -5.581506190343249,
            'Max. Drawdown Duration': str(pd.Timedelta('688 days 00:00:00')),
            'Avg. Drawdown Duration': str(pd.Timedelta('41 days 00:00:00')),
            '# Trades': 94,
            'Win Rate [%]': 54.25531914893617,
            'Best Trade [%]': 57.11930956177456,
            'Worst Trade [%]': -16.62989845236693,
            'Avg. Trade [%]': 2.0743259001844594,
            'Max. Trade Duration': str(pd.Timedelta('121 days 00:00:00')),
            'Avg. Trade Duration': str(pd.Timedelta('33 days 00:00:00')),
            'Profit Factor': 2.1908048949341876,
            'Expectancy [%]': 2.606294349683578,
            'SQN': 1.990216141635249}

    df = pd.Series(data).to_frame().reset_index()
    df = df.rename(columns={"index": "param", 0: ""})
    return df


if __name__ == '__main__':
    MOCK_PERFORMANCE_STATUS()
