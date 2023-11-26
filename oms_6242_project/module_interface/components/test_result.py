"""
This script produce test result context
"""
from module_core.container.BackTestInfo import NotionalInfo, PerformanceInfo
from module_utility.sample.mock import MOCK_PERFORMANCE_STATUS

from module_core.core import BTCore
from dash import html, dcc, dash_table
import pandas as pd
import plotly.express as px

DF_PERFORMANCE = MOCK_PERFORMANCE_STATUS()


def get_performance_test_result(df: pd.DataFrame):
    rics = df.ric.unique()
    first_ric = rics[0]
    test_result = html.Div([
        html.H2(children='BackTest Result',
                style={'textAlign': 'left', 'width': '90%', 'height': '30%', 'margin': '10px'}),
        dcc.Dropdown(rics, first_ric, id='dropdown-selection',
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


def get_single_stock_pnl_result(ric: str, df_stocks: pd.DataFrame):
    df_stock = df_stocks[ric].to_frame()
    df_stock = df_stock.rename(columns={ric: "pnl_pct"})
    df_stock["ric"] = ric
    df_plot = pd.concat([df_stock], axis=0)
    fig = px.line(df_plot, x=df_plot.index, y='pnl_pct', color="ric", title="Underlying performance")
    return fig


def get_portfolio_pnl_result(df_plot: pd.DataFrame):
    fig = px.line(df_plot, x=df_plot.index, y='total_return', color="ric", title="Portfolio performance")
    return fig
