from dash import Dash, dcc, html, Input, Output,State
from dash_bootstrap_components import themes
from dash_bootstrap_components.themes import BOOTSTRAP
import dash_bootstrap_components as dbc
from ids import * 
from Componet_View import render
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objects as go   
import Data_Processing as dp
import layout as ly
import Componet_View as cv
import dash_ag_grid as dag
import plotly as go
from plotly.subplots import make_subplots

list_of_files = dp.get_data(dp.path)                           
final_Value_df = dp.Create_Value_df(list_of_files)
final_volume_df = dp.Create_Volume_df(list_of_files)

data=list_of_files.get('SBK.JSE')
data = data.where(data['Open'] > 0) 

# 
# date=data['Date']
data['Open']=data['Open'] /100
price_line=dp.Price_line(data)
# print(data)
fig = make_subplots(
    rows=1, cols=1,
    shared_xaxes=True,
    vertical_spacing=0.02
    )
for i in price_line.data:
    fig.add_trace(i, row=1, col=1)




prices = pd.Series(data['Open'])

upper, lower, signals = dp.calculate_bollinger_bands(prices)
# print(upper)
x=pd.DataFrame()
x['time']=pd.to_datetime(data['Date'])


boundaries=dp.plot_line_graph(x,upper,lower,signals)

for i in boundaries.data:
    fig.add_trace(i, row=1, col=1)
fig.update_layout(title='Bollinger Bands with Signals',
                xaxis_title='Date',
                yaxis_title='Price/Signal',
                template="plotly_dark" 
                )
fig.show()    

# fig = make_subplots(
#     rows=2, cols=1,
#     shared_xaxes=True,
#     vertical_spacing=0.02
#     )
# # for i in boundaries:
# #     fig.add_trace(i, row=1, col=1)
    
# for i in price_line:
#     fig.add_trace(i, row=1, col=1)

# fig.show()


Names_jse_tickers= []
for key in list_of_files.keys():
    Names_jse_tickers.append(key)
    
df =final_Value_df #test 


new_df=pd.DataFrame()
series = pd.Series(Names_jse_tickers)
new_df= series.to_frame('Bank_Stock')

new_df.loc[0,'TOT_VALUE']=final_Value_df['CPI.JSE'].sum()
new_df.loc[1,'TOT_VALUE']=final_Value_df['SBK.JSE'].sum()
new_df.loc[2,'TOT_VALUE']=final_Value_df['FGL.JSE'].sum()
new_df.loc[3,'TOT_VALUE']=final_Value_df['ABG.JSE'].sum()
new_df.loc[4,'TOT_VALUE']=final_Value_df['NED.JSE'].sum()
new_df.loc[5,'TOT_VALUE']=final_Value_df['INP.JSE'].sum()

new_df.loc[0,'TOT_VOLUME']=final_volume_df['CPI.JSE'].sum()
new_df.loc[1,'TOT_VOLUME']=final_volume_df['SBK.JSE'].sum()
new_df.loc[2,'TOT_VOLUME']=final_volume_df['FGL.JSE'].sum()
new_df.loc[3,'TOT_VOLUME']=final_volume_df['ABG.JSE'].sum()
new_df.loc[4,'TOT_VOLUME']=final_volume_df['NED.JSE'].sum()
new_df.loc[5,'TOT_VOLUME']=final_volume_df['INP.JSE'].sum()


# app = Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME])
# app.title = "JSE"
# app.layout= html.Div(
#     [
#     dbc.NavbarSimple(
#         children=[
#             dbc.NavItem(dbc.NavLink("About", href="/about"), ),
#         ],
#         brand="Stock-Volume-Volatility",
#         brand_href="#",
#         color="primary",
#         dark=True,
#         style={"margin": 10, "height": "7vh",}
#     ),
#     dbc.Row([
#         html.Img(src='assets/Citi.png',style={'height': '3%',
#                     'width':'10%',
#                     'padding-right':70,
#                     'position':'relative'})]),
#     html.Label("Select JSE Bank Stock:", htmlFor="ticker", style={'textAlign':'center'}),
#     dbc.Row([
#         dbc.Col([dcc.Dropdown(id='ticker', value='CPI.JSE',clearable=True,options=Names_jse_tickers) ], width=5)
#     ]),       
#     dbc.Row([
#         dbc.Col([
#             dcc.Graph(id="time-series-chart", figure={})
#         ], width=12, md=6),
#         dbc.Col([
#         dbc.Row([dbc.Col([dcc.Graph(id='bar-graph-plotly', figure={}) ], width=12) ]),
#         ], width=12, md=6),
#         ], className='mt-4'),
#         # dcc.RadioItems(
#         #     id="selection",
#         #     options=[{"label": ticker, "value": ticker} for ticker in Names_jse_tickers],
#         #     value=Names_jse_tickers[0],
#         #     labelStyle={"display": "block"},
#         # ),
        
#     html.Label("Select JSE Bank Stock to Compare:", htmlFor="ticker", style={'textAlign':'center'}), 
#     dbc.Row([
#         dbc.Col([dcc.Dropdown(id='second-ticker', value='CPI.JSE',clearable=True,options=Names_jse_tickers) ], width=5)
#     ]),   
#     dbc.Row([dbc.Col([html.H1('time-serie')], width=12)]), 
#         dbc.Row([
#         dbc.Col([
#             dcc.Graph(id="second-time-series-chart", figure={})
#         ], width=12, md=6),
#         dbc.Col([
#         dbc.Row([dbc.Col([dcc.Graph(id='second-bar-graph-plotly', figure={}) ], width=12) ]),
#         ], width=12, md=6),
#         ], className='mt-4'),
        
#     ]
# )


# @app.callback(
#     Output("time-series-chart", "figure"), 
#     Output('bar-graph-plotly', 'figure'),
#     Input("ticker", "value"))

# def display_time_series(ticker):
#    # df = px.data.stocks() # replace with your own data source
#     df = final_Value_df
    
#     fig = px.line(df, x='Date', y=ticker)
#     fig.update_layout(title=f"{ticker} Value Over Time")
#     fig.layout.template = 'plotly_dark'
#     fig_bar_plotly = px.bar(new_df, x='Bank_Stock', y='TOT_VALUE').update_xaxes(tickangle=330)
#     # fig_bar_plotly.template = 'plotly_dark'
#     return fig,fig_bar_plotly

# @app.callback(
#     Output("second-time-series-chart", "figure"), 
#     Output('second-bar-graph-plotly', 'figure'),
#     Input("second-ticker", "value"))

# def display_time_series(ticker):
#    # df = px.data.stocks() # replace with your own data source
#     df = final_Value_df
    
#     fig = px.line(df, x='Date', y=ticker)
#     fig.update_layout(title=f"{ticker} Value Over Time")
#     fig.layout.template = 'plotly_dark'
#     fig_bar_plotly = px.bar(new_df, x='Bank_Stock', y='TOT_VOLUME').update_xaxes(tickangle=330)
#     # fig_bar_plotly.template = 'plotly_dark'
#     return fig,fig_bar_plotly



# app.run_server(debug=True)