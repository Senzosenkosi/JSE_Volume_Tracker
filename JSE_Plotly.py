from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
import re
import os

def process_file(file_path):
    
    #file_path='/Users/senzosenkosishezi/Desktop/JSE_Volume_Tracker/JSE_Volume_Tracker/Time Series (GND.JSE)_2025-03-01T22_32_02+02_00.csv'
    
    Date_trade_volume = re.search(r'\d{4}-\d{2}-\d{2}', file_path)
    cols=['Date','Open','High',	'Low','Close','Volume','Value','MktVWAP','Transactions','Adj. Factor']
    symbol_data= pd.read_csv(file_path,skiprows=0,usecols=cols)
    
    symbol_data['Date'] = pd.to_datetime(symbol_data['Date'])
    symbol_data['week' ] = symbol_data['Date'].dt.to_period('W').dt.to_timestamp()
    symbol_data['year'] = symbol_data['Date'].dt.year

    # symbol_data.set_index('Date', inplace=True)
    
    for index, row in symbol_data.iterrows():
        
        if 'k' in row['Volume']:
            row['Volume'] = row['Volume'].replace('k', '')
            row['Volume'] = float(row['Volume']) * 1000  
            symbol_data.at[index, 'Volume'] = row['Volume'] 
        elif 'm' in row['Volume']:
            row['Volume'] = row['Volume'].replace('m', '')
            row['Volume'] = float(row['Volume']) * 1000000
            symbol_data.at[index, 'Volume'] = row['Volume']
            
        if 'm' in row['Value']: 
            row['Value'] = row['Value'].replace('m', '')
            row['Value']= float(row['Value']) * 1000000
            symbol_data.at[index, 'Value'] = row['Value']
            
        elif 'k' in row['Value']:
            row['Value'] = row['Value'].replace('k', '')
            row['Value'] = float(row['Value']) * 1000
            symbol_data.at[index, 'Value'] = row['Value']

        if float(row['Value']) < 1000000:
            symbol_data.at[index, 'Value_group'] = 'Less than 1M'
        elif float(row['Value']) < 5000000 and float(row['Value']) > 1000000:
            symbol_data.at[index, 'Value_group']  = '1M to 5M'        
        elif float(row['Value']) < 10000000 and float(row['Value']) > 5000000:
            symbol_data.at[index, 'Value_group']  = '5M to 10M'
        elif float(row['Value']) < 100000000 and float(row['Value']) > 10000000:  
            symbol_data.at[index, 'Value_group']  = '10M to 100M'  
        else:
            symbol_data.at[index, 'Value_group']  = 'More than 100M'
    return symbol_data

def Create_Volume_df(list_of_files):
    
    final_volume_df = pd.DataFrame()
    date_df = pd.DataFrame()
    
    for key, value in list_of_files.items():
        date_df['date'] = value['Date']
        df=pd.DataFrame(value)
        final_volume_df[key] = df['Volume'].astype(float) / 1000   
            
    final_volume_df['Date'] = pd.to_datetime(date_df['date'])
    
    return final_volume_df

def Create_Value_df(list_of_files):
       
    final_Value_df = pd.DataFrame()
    date_df = pd.DataFrame()
    
    for key, value in list_of_files.items():       
        date_df['date'] = value['Date']
        df=pd.DataFrame(value)
        final_Value_df[key] = df['Value'].astype(float) / 1000000

    final_Value_df['Date'] = pd.to_datetime(date_df['date'])

    return final_Value_df

list_of_files={}
for x in os.listdir():
    if x.endswith(".csv") and 'Time Series' in x:   
       # print("file being processed is: ", x)
        JSE_symbol = re.search(r'\((.*?)\)', x)
        processed_file = process_file(x)
        list_of_files[JSE_symbol.group(1)] = processed_file
        
        

#print(list_of_files)              
final_Value_df = Create_Value_df(list_of_files)
final_volume_df = Create_Volume_df(list_of_files)
# final_df = final_Value_df.merge(final_volume_df, on='Date', how='inner')
# final_df.set_index('Date', inplace=True)
# final_df = final_df.resample('W').mean()
print(final_Value_df.head())
print(final_volume_df.head())

# app = Dash(__name__)

# app.layout = html.Div([
#     html.H4('Volume analysis Per stock'),
#     dcc.Graph(id="time-series-chart"),
#     html.P("Select stock:"),
#     dcc.Dropdown(
#         id="ticker",
#         options=["GND", "FB", "NFLX"],
#         value="AMZN",
#         clearable=False,
#     ),
# ])

# @app.callback(
#     Output("time-series-chart", "figure"), 
#     Input("ticker", "value"))

# def display_time_series(ticker):
#    # df = px.data.stocks() # replace with your own data source
#     df = symbol_data 
#     fig = px.line(df, x='Date', y='Open')
#     return fig

# app.run_server(debug=True)