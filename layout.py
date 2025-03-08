from dash import Dash, dcc, html, Input, Output
from dash_bootstrap_components import themes
from dash_bootstrap_components.themes import BOOTSTRAP
from ids import * 

import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objects as go   
import Data_Processing as dp
from Componet_View import render



def create_layout(app:Dash,Names_jse_tickers) -> html.Div:
    return html.Div([
    dcc.Store(id="stored-data", storage_type="memory"),  
    html.H1("JSE Volume Tracker"),
    html.H4('Volume Analysis Per stock'),
    dcc.Graph(id="time-series-chart"),
    html.P("Select stock:"),
    dcc.DatePickerSingle(
    id="single-start", clearable=True, display_format="YYYY-MM-DD"
    ),
    html.Div("End Date"),
    dcc.DatePickerSingle(
        id="single-end", clearable=True, display_format="YYYY-MM-DD"
    ),
    dcc.Dropdown(
        id="ticker",
        options=Names_jse_tickers,
        value='GND.JSE',
        clearable=False,
    ),html.Div(
            [
                html.H4(
                    "Step 2: Use the Date Picker Range to filter the data (within the date range) and update the graph"
                ),
                dcc.DatePickerRange(
                    id="range",
                    display_format="YYYY-MM-DD",
                ),
                dcc.Graph(id="graph"),
            ],
            hidden=True,
            id="graph-container",
        ),])
    
def render(app: Dash, Names_jse_tickers):
    return html.Div(
        children=[
            html.H1("Stocks"),
            dcc.Dropdown(
                options=[
                    {"label": ticker, "value": ticker} for ticker in Names_jse_tickers
                ],
                value=Names_jse_tickers[0],
                id=ids.SHARE_DROP_DOWN,
                multi=True,
            ),            
        ])    