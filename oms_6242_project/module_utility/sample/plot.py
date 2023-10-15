import numpy as np
import plotly.graph_objects as go


def plot() -> go.Figure:
    x = np.array([1, 2, 3, 4, 5])
    y = np.array([1, 3, 2, 3, 1])

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, name="linear",
                             line_shape='linear'))
    fig.add_trace(go.Scatter(x=x, y=y + 5, name="spline",
                             text=["tweak line smoothness<br>with 'smoothing' in line object"],
                             hoverinfo='text+name',
                             line_shape='spline'))
    fig.add_trace(go.Scatter(x=x, y=y + 10, name="vhv",
                             line_shape='vhv'))
    fig.add_trace(go.Scatter(x=x, y=y + 15, name="hvh",
                             line_shape='hvh'))
    fig.add_trace(go.Scatter(x=x, y=y + 20, name="vh",
                             line_shape='vh'))
    fig.add_trace(go.Scatter(x=x, y=y + 25, name="hv",
                             line_shape='hv'))

    fig.update_traces(hoverinfo='text+name', mode='lines+markers')
    fig.update_layout(legend=dict(y=0.5, traceorder='reversed', font_size=16))
    return fig
