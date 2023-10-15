"""
This script is Portfolio Uploader Component
"""

from dash import dash_table, html, dcc, callback
import pandas as pd
from dash.dependencies import Input, Output




DATA_TABLE_UPLOAD_CONTAINER = 'datatable-upload-container'
DATA_TABLE_UPLOAD_GRAPH = 'datatable-upload-graph'


def generate_upload_csv_table(df: pd.DataFrame):
    """
    :param df:
    :return:
    """
    table_div = html.Div(
        [
            html.Hr(),
            html.H3(children='Portfolio Constitutes', style={'textAlign': 'left'}),
            html.Hr(),
            dash_table.DataTable(
                id=DATA_TABLE_UPLOAD_CONTAINER,
                data=df.to_dict('records'),
                columns=[{'name': i, 'id': i} for i in df.columns],
                style_table={'overflowX': 'auto',
                             'width': '90%',
                             'margin': '10px',
                             'height': '30%'},
                css=[{'selector': 'table', 'rule': 'table-layout: fixed'}],
                style_cell={
                    'width': '{}%'.format(len(df.columns)),
                    'textOverflow': 'ellipsis',
                    'overflow': 'hidden',
                    'textAlign': 'left',
                },
                page_size=10,
                filter_action="native",
                sort_action="native",
                sort_mode="multi"
            ),
            dcc.Graph(id=DATA_TABLE_UPLOAD_GRAPH, style={'margin': '10px', 'width': '90%', 'height': '30%'}),
            html.Hr(),
        ])
    return table_div


def generate_consituent_weight(df: pd.DataFrame):
    if (df.empty or len(df.columns) < 1):
        return {
            'data': [{
                'x': [],
                'y': [],
                'type': 'bar'
            }]
        }
    return {
        'data': [{
            'x': df[df.columns[0]],
            'y': df[df.columns[1]],
            'type': 'bar'
        }]}


@callback(
    Output('output-data-upload', 'children'),
    Input('store', 'data')
)
def output_from_store(stored_data):
    df = pd.read_json(stored_data, orient='split')
    return generate_upload_csv_table(df=df)


@callback(Output(DATA_TABLE_UPLOAD_GRAPH, 'figure'),
          Input(DATA_TABLE_UPLOAD_CONTAINER, 'data'))
def display_graph(data):
    df = pd.DataFrame(data)
    return generate_consituent_weight(df=df)
