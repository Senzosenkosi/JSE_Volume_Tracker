# Description: This file contains functions that process the data from the csv files
# and create dataframes that can be used to create visualizations. The functions in this file
import pandas as pd
import numpy as np
import re
import os
import plotly.graph_objects as go



path = '/Users/senzosenkosishezi/Desktop/JSE_Volume_Tracker/JSE_Volume_Tracker'

def process_file(file_path):
    
   # file_path='/Users/senzosenkosishezi/Desktop/JSE_Volume_Tracker/JSE_Volume_Tracker/Time Series (GND.JSE)_2025-03-01T22_32_02+02_00.csv'
    
    Date_trade_volume = re.search(r'\d{4}-\d{2}-\d{2}', file_path)
    cols=['Date','Open','High',	'Low','Close','Volume','Value','MktVWAP','Transactions','Adj. Factor']
    symbol_data= pd.read_csv(file_path,skiprows=0,usecols=cols)
    
    symbol_data['Date'] = pd.to_datetime(symbol_data['Date'])
    symbol_data['week' ] = symbol_data['Date'].dt.to_period('W').dt.to_timestamp()
    symbol_data['year'] = symbol_data['Date'].dt.year

    # symbol_data.set_index('Date', inplace=True)
    
    for index, row in symbol_data.iterrows():
        
        if isinstance(row['Volume'],str) or isinstance(row['Value'],str):      
            if 'k' in row['Volume']:
                row['Volume'] = row['Volume'].replace('k', '')
                row['Volume'] = float(row['Volume']) * 1000  
                symbol_data.at[index, 'Volume'] = row['Volume'] 
            elif 'm' in row['Volume']:
                row['Volume'] = row['Volume'].replace('m', '')
                row['Volume'] = float(row['Volume']) * 1000000
                symbol_data.at[index, 'Volume'] = row['Volume']
                
            elif 'b' in row['Value']: 
                row['Value'] = row['Value'].replace('b', '')
                row['Value']= float(row['Value']) * 1000000000
                symbol_data.at[index, 'Value'] = row['Value']   
                                
            if 'm' in row['Value']:
                row['Value'] = row['Value'].replace('m', '')
                row['Value']= float(row['Value']) * 1000000
                symbol_data.at[index, 'Value'] = row['Value']
                
            elif 'k' in row['Value']:
                row['Value'] = row['Value'].replace('k', '')
                row['Value'] = float(row['Value']) * 1000
                symbol_data.at[index, 'Value'] = row['Value']
            elif 'b' in row['Value']: 
                row['Value'] = row['Value'].replace('b', '')
                row['Value']= float(row['Value']) * 1000000000
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


def calculate_bollinger_bands(prices, window=7, num_std_dev=2):
    """
    Calculates Bollinger Bands and mean reversion signals.

    Args:
        prices (pd.Series): Time series of prices.
        window (int): Rolling window size.
        num_std_dev (float): Number of standard deviations for bands.

    Returns:
        tuple: (upper_band, lower_band, signals)
    """
    rolling_mean = prices.rolling(window).mean()
    rolling_std = prices.rolling(window).std()

    upper_band = rolling_mean + (rolling_std * num_std_dev)
    lower_band = rolling_mean - (rolling_std * num_std_dev)

    signals = pd.Series(0, index=prices.index)
    signals[prices > upper_band] = -1  # Short signal
    signals[prices < lower_band] = 1  # Long signal

    return upper_band, lower_band, signals

# Example usage:

def Price_line(data:pd.DataFrame):
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], mode='lines',line=dict(width=3), name='Prices'))
    
    return fig


def plot_line_graph(date,upper_band,lower_band,signals):
    
    fig = go.Figure()
    # Plot the original prices
    #fig.add_trace(go.Scatter(x=prices.index, y=prices, mode='lines', name='Prices'))

    # Plot the upper Bollinger Band
    fig.add_trace(go.Scatter(x=date['time'], y=upper_band, mode='lines', name='Upper Band'))

    # Plot the lower Bollinger Band
    fig.add_trace(go.Scatter(x=date['time'], y=lower_band, mode='lines', name='Lower Band'))

    # Plot the signals as a separate line
    fig.add_trace(go.Scatter(x=date['time'], y=signals, mode='lines', name='Signals',line=dict(width=2) ))

    fig.update_layout(title='Bollinger Bands with Signals',
                      xaxis_title='Date',
                      yaxis_title='Price/Signal',
                      template="plotly_dark" 
                      )
    return fig





def Create_Volume_df(list_of_files):
    
    final_Volume_df = pd.DataFrame()
    date_df = pd.DataFrame()
    
    for key, value in list_of_files.items():
        date_df['date'] = value['Date']
        df=pd.DataFrame(value)
        final_Volume_df[key] = df['Volume'].astype(float) / 1000   
            
    final_Volume_df['Date'] = pd.to_datetime(date_df['date'])
    
    return final_Volume_df

def Create_Value_df(list_of_files):
       
    final_Value_df = pd.DataFrame()
    date_df = pd.DataFrame()
    
    for key, value in list_of_files.items():       
        date_df['date'] = value['Date']
        df=pd.DataFrame(value)
        final_Value_df[key] = df['Value'].astype(float) / 1000000

    final_Value_df['Date'] = pd.to_datetime(date_df['date'])

    return final_Value_df


def get_data(path):
    os.chdir(path)
    list_of_files={}
    for x in os.listdir():
        if x.endswith(".csv") and 'Time Series' in x:   
            #print("file being processed is: ", x)
            JSE_symbol = re.search(r'\((.*?)\)', x)
            processed_file = process_file(x)
            list_of_files[JSE_symbol.group(1)] = processed_file
    return list_of_files


