"""
This script is side bar component
"""

from module_interface.components.constant import CLICK_BUTTOM_STYLE, UPLOAD_FILE_STYLE, DATE_BUTTOM_SYTLE, \
    STRATEGY_BUTTOM_SYTLE, INPUT_TEXT_STYLE

import dash_bootstrap_components as dbc
from datetime import date
from dash import Dash, html, dcc, callback
from dash.dependencies import Input, Output, State

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "50rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

DATE_PICKER_START = 'my-date-picker-single-start'
DATE_CONTAINER_PICKER_START = 'output-container-date-picker-single-start'
DATE_PICKER_END = 'my-date-picker-single-end'
DATE_CONTAINER_PICKER_END = "output-container-date-picker-single-end"
PORTFOLIO_NOTIONAL_INPUT = "portfolio-notional-input"
PORTFOLIO_NOTIONAL_OUTPUT = "portfolio-notional-output"
BACKTEST_RESULT = "backtest-result"
RUN_BACK_TEST = "run-back-test"
STORED_PORTFOLIO = "stored-portfolio"
STRATEGY_DROPDOWN = 'strategy-dropdown-selection'
CONTAINER_BUTTOM_BASIC = "container-button-basic"

SIDE_BAR = html.Div(
    [
        html.H2(
            "Control Panel", className="lead"
        ),
        html.Hr(),
        dbc.Nav(
            [html.Button('Run', id=RUN_BACK_TEST, n_clicks=0, style=CLICK_BUTTOM_STYLE),
             dcc.Upload(
                 id='upload-data',
                 children=html.Div(['Upload your portfolio file']),
                 style=UPLOAD_FILE_STYLE,
             ),
             dcc.Store(id=STORED_PORTFOLIO),
             html.P("Portfolio Notional in USD", style={"font-weight": "bold"}),
             dcc.Input(
                 id=PORTFOLIO_NOTIONAL_INPUT,
                 type="number",
                 placeholder="Portfolio Notional",
                 style=INPUT_TEXT_STYLE,
             )
             ]),
        html.P("Select your strategy", style={"font-weight": "bold"}),
        dcc.Dropdown(["BuyHold", "AutoRebalance"], 'BuyHold', id=STRATEGY_DROPDOWN,
                     style=STRATEGY_BUTTOM_SYTLE),
        html.P("Select Trade Start Date", style={"font-weight": "bold"}),
        html.Div(id=DATE_CONTAINER_PICKER_START),
        dcc.DatePickerSingle(
            id=DATE_PICKER_START,
            min_date_allowed=date(1995, 8, 5),
            max_date_allowed=date(2023, 9, 19),
            initial_visible_month=date(2023, 6, 1),
            date=date(2023, 6, 1),
            style=DATE_BUTTOM_SYTLE,
            placeholder="Start Test Day"
        ),
        html.P("Select Trade End Date", style={"font-weight": "bold"}),
        html.Div(id=DATE_CONTAINER_PICKER_END),
        dcc.DatePickerSingle(
            id=DATE_PICKER_END,
            min_date_allowed=date(1995, 8, 5),
            max_date_allowed=date(2023, 9, 19),
            initial_visible_month=date(2017, 8, 5),
            date=date(2023, 6, 30),
            style=DATE_BUTTOM_SYTLE,
            placeholder="End Test Day"
        ),
        dcc.Store(id=BACKTEST_RESULT)
    ],
    style=SIDEBAR_STYLE
)


@callback(
    Output(DATE_CONTAINER_PICKER_START, 'children'),
    Input(DATE_PICKER_START, 'date'))
def get_test_start_date(date_value) -> str:
    string_prefix = 'Start Test Day: '
    if date_value is not None:
        date_object = date.fromisoformat(date_value)
        date_string = date_object.strftime('%B %d, %Y')
        return string_prefix + date_string


@callback(
    Output(DATE_CONTAINER_PICKER_END, 'children'),
    Input(DATE_PICKER_END, 'date'))
def get_test_end_date(date_value) -> str:
    string_prefix = 'End Test Day: '
    if date_value is not None:
        date_object = date.fromisoformat(date_value)
        date_string = date_object.strftime('%B %d, %Y')
        return string_prefix + date_string


@callback(
    Output(PORTFOLIO_NOTIONAL_OUTPUT, 'children'),
    Input(PORTFOLIO_NOTIONAL_INPUT, 'value'))
def get_test_portfolio_notional(notional_usd) -> float:
    return notional_usd
