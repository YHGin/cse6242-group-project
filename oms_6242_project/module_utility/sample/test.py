"""
This is python test script
"""

import pandas as pd
import plotly.graph_objects as go
from module_datalayer.reader import get_stock_price, get_index_price


def test_run():
    rics = ["00001HK", "00002HK"]
    start_date = pd.Timestamp("2004-01-01")
    end_date = pd.Timestamp("2010-01-01")
    df_bag = get_stock_price(rics, start_date, end_date)

    rics = ["00001HK", "00002HK"]
    allocation_pct = [.5, .5]
    fig = go.Figure(data=[go.Pie(labels=rics, values=allocation_pct)])
    fig.update_layout(title="Portfolio Asset Allocation")
    fig.show()

    # Calculate the cumulative return
    for ric in df_bag.keys():
        df = df_bag.get(ric)
        df['Cum Return'] = df['Close'] / df.iloc[0]['Close']


if __name__ == '__main__':
    test_run()
