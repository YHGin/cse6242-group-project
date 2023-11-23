"""
This script is Content Component
"""

from module_interface.components.side_bar import DATE_PICKER_START, DATE_PICKER_END, PORTFOLIO_NOTIONAL_INPUT, \
    RUN_BACK_TEST, BACKTEST_RESULT, CONTAINER_BUTTOM_BASIC
from module_interface.components.test_result import get_performance_test_result, get_single_stock_pnl_result, \
    get_portfolio_pnl_result
from module_core.buyhold import BuyHoldBT, DB_PATH, PerformanceInfo
from dash import html, dcc, callback
import pandas as pd
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import base64
import io

CONTENT_STYLE = {
    "margin-left": "55rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}
BACK_TEST_RESULT = "back-test-result"

BACK_TEST_OBJ = None

CONTENT = html.Div(id="page-content",
                   children=
                   [
                       html.H1(children='OMS BackTestor', style={'textAlign': 'left'}),
                       dcc.Store(id='store'),
                       html.Div(id='output-data-upload'),
                       html.Div(id=CONTAINER_BUTTOM_BASIC),
                       html.Hr(),
                       html.Div(id=BACK_TEST_RESULT),
                   ],
                   className="p-3 bg-light rounded-3",
                   style=CONTENT_STYLE
                   )


@callback(Output('store', 'data'),
          Input('upload-data', 'contents'),
          State('upload-data', 'filename'),
          State('upload-data', 'last_modified'))
def update_output(contents, list_of_names, list_of_dates):
    if contents is None:
        raise PreventUpdate
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
    return df.to_json(date_format='iso', orient='split')


@callback(
    [Output(CONTAINER_BUTTOM_BASIC, 'children'),
     Output(BACKTEST_RESULT, 'data')],
    [
        Input(RUN_BACK_TEST, 'n_clicks'),
        State('store', 'data'),
        State(DATE_PICKER_START, 'date'),
        State(DATE_PICKER_END, 'date'),
        State(PORTFOLIO_NOTIONAL_INPUT, 'value')],
    prevent_initial_call=True
)
def update_output(n_clicks, data, start_date, end_date, portfolio_notional):
    df = pd.read_json(data, orient='split')
    df = df[["ric", "side", "qty"]]
    print("doing test")
    buyhold_test = BuyHoldBT(start_date=start_date, end_date=end_date, path=DB_PATH, df_portfolio=df)
    buyhold_test.run()
    df_portfolio_metrix = buyhold_test.get_portfolio_metric(field=PerformanceInfo.PriceChange.value)
    result_json = df_portfolio_metrix.to_json(orient='split')
    test_result = get_performance_test_result(df=df)
    return test_result, result_json


@callback(
    Output('graph-single-stock-pnl_chart', 'figure'),
    [Input('dropdown-selection', 'value'),
     Input(BACKTEST_RESULT, 'data')]

)
def update_underlying_graph(value,data):
    df_portfolio = pd.read_json(data, orient='split')
    # TODO need better result, but now just make it runnable
    pnl_result = get_single_stock_pnl_result(ric=value,df_portfolio=df_portfolio)
    return pnl_result


@callback(
    Output('graph-portfolio-pnl_chart', 'figure'),
    [Input('dropdown-selection', 'value'),
     Input(BACKTEST_RESULT, 'data')]
)
def update_portfolio_graph(value,data):
    df_portfolio = pd.read_json(data, orient='split')
    # TODO too late on Thursday night, actually it already Friday.. I yiwei will add real function here, or anyone want to help here?
    # get_portfolio_pnl_result(df_portfolio)
    return get_single_stock_pnl_result(ric=value,df_portfolio=df_portfolio)
