"""
This script produce test result context
"""

from module_utility.sample.mock import MOCK_PERFORMANCE_STATUS, MOCK_PNL_RESULT

from dash import html, dcc, dash_table
import pandas as pd
import plotly.express as px

DF_PERFORMANCE = MOCK_PERFORMANCE_STATUS()
DF_STOCK, DF_BENCHMARK = MOCK_PNL_RESULT()


def get_performance_test_result(df: pd.DataFrame):
    test_result = html.Div([
        html.H2(children='BackTest Result',
                style={'textAlign': 'left', 'width': '90%', 'height': '30%', 'margin': '10px'}),
        dcc.Dropdown(DF_STOCK.ric.unique(), '00001.HK', id='dropdown-selection',
                     style={'margin': '10px', 'width': '45%'}),
        html.H3(children='Performance PNL Percentage',
                style={'textAlign': 'left', 'width': '90%', 'height': '30%', 'margin': '10px'}),
        html.Div(children=[
            dcc.Graph(id='graph-single-stock-pnl_chart', style={'display': 'inline-block', 'width': '45%'}),
            dcc.Graph(id='graph-portfolio-pnl_chart', style={'display': 'inline-block', 'width': '45%'}),
        ]),
        html.H3(children='Performance Status',
                style={'textAlign': 'left', 'width': '90%', 'height': '30%', 'margin': '10px'}),
        dash_table.DataTable(
            data=DF_PERFORMANCE.to_dict('records'),
            columns=[{'id': c, 'name': c} for c in DF_PERFORMANCE.columns],
            style_table={'overflowX': 'auto',
                         'width': '90%',
                         'margin': '10px',
                         'height': '30%'},
            css=[{'selector': 'table', 'rule': 'table-layout: fixed'}],
            style_cell={
                'width': '40%',
                'textOverflow': 'ellipsis',
                'overflow': 'hidden',
                'font-size': '20px',
                'textAlign': 'left',
            },
            style_data={
                'color': 'black',
                'backgroundColor': 'white'
            },
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(220, 220, 220)',
                }
            ],

            style_header={
                'backgroundColor': 'rgb(210, 210, 210)',
                'color': 'black',
                'fontWeight': 'bold'
            },
            style_cell_conditional=[
                {
                    'if': {'column_id': 'param'},
                    'textAlign': 'left',
                    'fontWeight': 'bold',
                    'font-size': '25px',
                }]
        )
    ])
    return test_result


def get_single_stock_pnl_result(ric: str):
    df_stock = DF_STOCK[DF_STOCK.ric == ric]
    df_plot = pd.concat([df_stock, DF_BENCHMARK], axis=0)
    fig = px.line(df_plot, x=df_plot.index, y='pnl_pct', color="ric", title="Underlying performance")
    return fig


def get_portfolio_pnl_result(df: pd.DataFrame):
    fig = px.line(DF_BENCHMARK, x=DF_BENCHMARK.index, y='pnl_pct', color="ric", title="Portfolio performance")
    return fig
