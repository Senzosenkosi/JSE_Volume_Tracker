from dash import Dash, dcc, html, Input, Output
from dash_bootstrap_components import themes
from dash_bootstrap_components.themes import BOOTSTRAP
import ids as ids

import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objects as go   
import Data_Processing as dp


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