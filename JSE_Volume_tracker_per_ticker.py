import seaborn as sns
import os
import pandas as pd
import numpy as np
import re
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import matplotlib.ticker as ticker
import mplcursors
import matplotlib.dates as mdates

# Replace 'your_file.xlsx' with the path to your Excel file
#file_path = '/path/to/your_file.xlsx' 

def process_file(file_path):
    
    #file_path='/Users/senzosenkosishezi/Desktop/JSE_Volume_Tracker/JSE_Volume_Tracker/Time Series (GND.JSE)_2025-03-01T22_32_02+02_00.csv'
    JSE_symbol = re.search(r'\((.*?)\)', file_path)
    Date_trade_volume = re.search(r'\d{4}-\d{2}-\d{2}', file_path)
    cols=['Date','Open','High',	'Low','Close','Volume','Value','MktVWAP','Transactions','Adj. Factor']
    symbol_data= pd.read_csv(file_path,skiprows=0,usecols=cols)
    symbol_data['JSE_symbol'] = JSE_symbol.group(1)

    symbol_data['Date'] = pd.to_datetime(symbol_data['Date'])
    symbol_data['week' ] = symbol_data['Date'].dt.to_period('W').dt.to_timestamp()
    symbol_data['year'] = symbol_data['Date'].dt.year

    symbol_data.set_index('Date', inplace=True)
    
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
    
def plt__line_graph(symbol_data):
    plt.figure(figsize=(12, 6))  # Set the size of the plot
    line1=plt.plot(symbol_data['Value'], label='Volume', color='Green')    
    plt.title(symbol_data['JSE_symbol'].unique() + " " +'Traded Volume Over Time')
    plt.xlabel('Date')
    plt.ylabel('Volume Traded in millions')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.8) # Add a grid for easier reading
        
    plt.tight_layout() #prevents labels from being cut off
    
    
    def show_info(sel):
        x, y = sel.target
        xdata = sel.artist.get_xdata()
        ydata = sel.artist.get_ydata()
        x_datetime = pd.to_datetime(x, unit='ms').to_numpy()
        index = (np.abs(xdata - x_datetime)).argmin()
        date = sel.artist.get_xdata()[index]
        volume = sel.artist.get_ydata()[index]
        share_name = sel.artist.get_label()

        # Convert numpy.datetime64 to Python datetime
        date_py = pd.to_datetime(date).to_pydatetime()

        sel.annotation.set_text(f"{share_name}\n at Date: {date_py.strftime('%Y-%m-%d')}\nVolume: {volume:.2f}")   
    
    mplcursors.cursor(line1, hover=True).connect("add", show_info)
    
    plt.show()  # Display the plot


def bar_graph(symbol_data):
    symbol_data['Value_group'] = symbol_data['Value_group'].astype('category')

    list_ordering = ["Less than 1M", "1M to 5M", "5M to 10M", "10M to 100M", "More than 100M"]
    symbol_data['Value_group'].cat.reorder_categories(list_ordering)
    #symbol_data["Value_group"] = symbol_data["Value_group"].astype("category", Value_group=list_ordering, ordered=True)
    sns.set_theme(style="whitegrid")
    sns.barplot(x="Value_group", y="Volume", data=symbol_data, order=list_ordering)
    plt.title('GND.JSE Traded Volume Grouped by Value')
    plt.xlabel('Value Group')
    plt.ylabel('Volume Traded')
    plt.show()


def diff_graph(symbol_data):
    symbol_data['Value_group'] = symbol_data['Value_group'].astype('category')

    list_ordering = ["Less than 1M", "1M to 5M", "5M to 10M", "10M to 100M", "More than 100M"]
    symbol_data['Value_group'].cat.reorder_categories(list_ordering)    
    sns.catplot(data=symbol_data, x="week", y="Value_group")
    plt.show()

def lblFormat(n, pos):
    return str(int(n / 1e6))
    
def Bar_view(symbol_data):
    
    n, bins, patches = plt.hist(x=symbol_data['Value_group'], bins=10, color='#0504aa',
                            alpha=0.7, rwidth=0.85)
    maxfreq = n.max()
    plt.ylim(ymax=np.ceil(maxfreq / 10) * 10 if maxfreq % 10 else maxfreq + 10)

    # lblFormatter = FuncFormatter(lblFormat)
    # ax = symbol_data.Val.plot.bar(rot=0, width=0.75)
    # ax.yaxis.set_major_formatter(lblFormatter)
    plt.show()

list_of_files = []   
final_df = pd.DataFrame()
for x in os.listdir():
    if x.endswith(".csv") and 'Time Series' in x:   
        print("file being processed is: ", x)
        processed_file = process_file(x)
        list_of_files.append(processed_file)
       # plt__line_graph(processed_file)
        #bar_graph(processed_file)
        # diff_graph(processed_file)
        #Bar_view(processed_file)


# plot_stock_volumes(list_of_files[0], list_of_files[1], 'GND.JSE', 'GND.JSE', 
#                    volume_column1='Volume', volume_column2='Volume',
#                    title='Stock Volume Traded', date_format='%Y-%m-%d')