"""
for this front end interface, please vist https://dash.plotly.com/ to add componenets
The goal is to replicate line chart like /module_interface/resource/backtest_sample.html along with a performance table
"""
from module_interface.components.content import CONTENT
from module_interface.components.side_bar import SIDE_BAR
from module_interface.components.portfolio_uploader import generate_upload_csv_table, generate_consituent_weight, \
    output_from_store, display_graph

from dash import Dash, html, dcc


def app_run():
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    app = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=external_stylesheets)
    sidebar = SIDE_BAR
    content = CONTENT
    app.layout = html.Div([dcc.Location(id="url"), sidebar, content])
    app.run(debug=True)


if __name__ == '__main__':
    app_run()
