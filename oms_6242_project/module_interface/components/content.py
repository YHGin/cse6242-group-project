"""
This script is Content Component
"""

from module_interface.components.side_bar import DATE_PICKER_START, DATE_PICKER_END, PORTFOLIO_NOTIONAL_INPUT, \
    RUN_BACK_TEST
from module_interface.components.test_result import get_performance_test_result, get_single_stock_pnl_result, \
    get_portfolio_pnl_result

from module_datalayer.writer import DbWriter

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
CONTENT = html.Div(id="page-content",
                   children=
                   [
                       html.H1(children='OMS BackTestor', style={'textAlign': 'left'}),
                       dcc.Store(id='store'),
                       html.Div(id='output-data-upload'),
                       html.Div(id='container-button-basic'),
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
    db_writer = DbWriter(path="./module_datalayer/resource/db/backtest_db")
    db_writer.write_csv_data(table_name="stock_price", df=df, ric="00001.HK")
    db_writer.write_csv_data(table_name="stock_price", df=df, ric="00002.HK")
    return df.to_json(date_format='iso', orient='split')

@callback(
    Output('container-button-basic', 'children'),
    [
        Input(RUN_BACK_TEST, 'n_clicks'),
        State('store', 'data'),
        State(DATE_PICKER_START, 'date'),
        State(DATE_PICKER_END, 'date'),
        State(PORTFOLIO_NOTIONAL_INPUT, 'value')],
    prevent_initial_call=True
)
def update_output(n_clicks, data, start_date, end_date, portfolio_notional):
    df = pd.DataFrame()
    return get_performance_test_result(df=df)


@callback(
    Output('graph-single-stock-pnl_chart', 'figure'),
    Input('dropdown-selection', 'value', )
)
def update_underlying_graph(value):
    return get_single_stock_pnl_result(ric=value)


@callback(
    Output('graph-portfolio-pnl_chart', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_portfolio_graph(value):
    df = pd.DataFrame()
    return get_portfolio_pnl_result(df=df)
