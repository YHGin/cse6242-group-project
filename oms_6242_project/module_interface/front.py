
"""
for this front end interface, please vist https://dash.plotly.com/ to add componenets (I spent one and half hour and got below stuff already, very easy)
our goal is to replicate line chart like /module_interface/resource/backtest_sample.html
along with a performance table
"""

from dash import Dash, html, dcc, callback, Output, Input, dash_table
import plotly.express as px
import pandas as pd
from module_core.container.stock import run_stock_test
from typing import Union
from module_utility.sample.mock import MOCK_PERFORMANCE_STATUS
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import base64
import io


def mock_pnl_result() -> Union[pd.DataFrame, pd.DataFrame]:
    df_stock_0 = run_stock_test('00001.HK')
    df_stock_1 = run_stock_test('00002.HK')
    df_bechmark = run_stock_test('.HSI')
    df = pd.concat([df_stock_0, df_stock_1], axis=0)
    return df, df_bechmark


def app_run():
    app = Dash(__name__,suppress_callback_exceptions=True)
    app.layout = html.Div([
        html.H1(children='OMS BackTest', style={'textAlign': 'left'}),
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Upload you portfolio .csv ',
                html.A('Select Files')
            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            },
        ),
        dcc.Store(id='store'),
        html.Div(id='output-data-upload'),
        html.Div(dcc.Input(id='input-on-submit', type='text')),
        html.Button('Run', id='submit-val', n_clicks=0),
        html.Div(id='container-button-basic', children='Enter a value and press submit'),
    ])
    app.run(debug=True)


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
    Output('output-data-upload', 'children'),
    Input('store', 'data')
)
def output_from_store(stored_data):
    df = pd.read_json(stored_data, orient='split')
    return html.Div(
        [dash_table.DataTable(df.to_dict('records'), [{'name': i, 'id': i} for i in df.columns]), html.Hr(), ])


DF_PERFORMANCE = MOCK_PERFORMANCE_STATUS()
DF_STOCK, DF_BENCHMARK = mock_pnl_result()


@callback(
    Output('container-button-basic', 'children'),
    Input('submit-val', 'n_clicks'),
    State('input-on-submit', 'value'),
    prevent_initial_call=True
)
def update_output(n_clicks, value):
    result = html.Div([
        html.H2(children='BackTest Result', style={'textAlign': 'left'}),
        html.H3(children='Portfolio performance', style={'textAlign': 'left'}),
        html.H3(children='Underlying performance', style={'textAlign': 'left'}),
        dcc.Dropdown(DF_STOCK.ric.unique(), '00001.HK', id='dropdown-selection'),
        dcc.Graph(id='graph-pnl_chart'),
        dash_table.DataTable(
            data=DF_PERFORMANCE.to_dict('records'),
            columns=[{'id': c, 'name': c} for c in DF_PERFORMANCE.columns],
            style_cell_conditional=[
                {'if': {'column_id': 'param'}, 'width': '20%'},
                {'if': {'column_id': ''}, 'width': '70%'},
            ],
            fill_width=False
        )
    ])
    return result


@callback(
    Output('graph-pnl_chart', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph(value):
    df_stock = DF_STOCK[DF_STOCK.ric == value]
    df_plot = pd.concat([df_stock, DF_BENCHMARK], axis=0)
    fig = px.line(df_plot, x=df_plot.index, y='pnl_pct', color="ric")
    return fig


if __name__ == '__main__':
    app_run()
