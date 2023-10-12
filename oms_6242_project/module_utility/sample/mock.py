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


def test():
    df_stock = MOCK_DATA("00001HK")
    print(df_stock.head(3))
    df_index = MOCK_INDEX_DATA("HSI")
    print(df_index.head(3))


if __name__ == '__main__':
    test()
