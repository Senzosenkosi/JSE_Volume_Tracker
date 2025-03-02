import seaborn as sns
import os
import pandas as pd
import numpy as np
import re
from datetime import datetime
import matplotlib.pyplot as plt

# Replace 'your_file.xlsx' with the path to your Excel file
#file_path = '/path/to/your_file.xlsx' 

def process_file(file_path):
    # Read the CSV file
    file_path='/Users/senzosenkosishezi/Desktop/JSE_Volume_Tracker/JSE_Volume_Tracker/Time Series (GND.JSE)_2025-03-01T22_32_02+02_00.csv'
   #file_path ='/Users/senzosenkosishezi/Desktop/JSE_Volume_Tracker/JSE_Volume_Tracker/Course of Sales (GRT.JSE)_2025-02-27T17_05_47+02_00.csv'
    JSE_symbol = re.search(r'\((.*?)\)', file_path)
    Date_trade_volume = re.search(r'\d{4}-\d{2}-\d{2}', file_path)
    cols=['Date','Open','High',	'Low','Close','Volume','Value','MktVWAP','Transactions','Adj. Factor']
    symbol_data= pd.read_csv(file_path,skiprows=0,usecols=cols)
    # symbol_data=symbol_data.where(symbol_data['Date'] > '10-Feb-25')
    #print(symbol_data['Date'].to_timestamp())
    # symbol_data['Date'] = pd.to_datetime(symbol_data['Date'])  
    sns.relplot(
    data=symbol_data, x="Date", y="Value",
    size="Date", sizes=(15, 200)
    )
    plt.show()
    
    # sns.relplot(x='Value', y='Date', data=symbol_data,hue='Date',kind='scatter')
    # # sns.lineplot(data=symbol_data.where(symbol_data['Date'] > '10-Feb-25'), x='Date', y='Value', marker='o')
    # # plt.title(f'Value Over Time for {JSE_symbol}')
    # # plt.xlabel('Date')
    # # plt.ylabel('Value')
    # # plt.xticks(rotation=45)
    # plt.show()
    
    # Replace empty strings with NaN
    # symbol_data.replace(r'^\s*$', np.nan, regex=True, inplace=True)
    
    # symbol_data.replace(r'^\s*$', np.nan, regex=True)
    # symbol_data['Traded_Volume'] = symbol_data['Value'].replace('-', 'MATCH')
    # # Replace '-' with 'MATCH' in 'Value' column
    
    
    # symbol_data['Rand_Value'] = symbol_data['Volume'].str.split('  ', expand=True)
    # symbol_data['Rand_Value']=symbol_data['Rand_Value'].astype(str)
    # symbol_data['Rand_Value']=symbol_data['Rand_Value'].replace(',','',regex=True)
    # symbol_data['Rand_Value']=symbol_data['Rand_Value'].astype(float)

    # aggregated_volume = symbol_data.groupby('Traded_Volume')['Rand_Value'].sum()
    
    # Total_ASK = aggregated_volume['ASK']
    # Total_BID = aggregated_volume['BID']
    # Total_MATCH = aggregated_volume['MATCH']
    
    
    # share_data_info_per_date= aggregated_volume.to_list()
    # share_data_info_per_date.append(JSE_symbol.group(1))
    # share_data_info_per_date.append(Date_trade_volume.group())
    # share_data_info_per_date.append(Total_ASK+Total_BID+Total_MATCH)
    # # final_Data = ['BID','ASK','MATCH']
    
    # return share_data_info_per_date
   
    
    # dicti={'TOT_BID':0,'TOT_ASK':0,'MATCH':0,'SYMBOL':0,'Date':0}
    
    # share_data_info_per_date['SYMBOL'] = JSE_symbol.group(1)
    # share_data_info_per_date['Date'] = Date_trade_volume.group()
    #share_data_info_per_date = pd.DataFrame([share_data_info_per_date])
    
    
    #share_data_info_per_date=pd.DataFrame(share_data_info_per_date.items(), columns=['ASK', 'Date'])
    
   # print(share_data_info_per_date)
  
    
    # melted_df = share_data_info_per_date.melt(id_vars=['SYMBOL', 'Date'], var_name='Type', value_name='Volume')
    # # sns.barplot(data=melted_df, x='SYMBOL', y='Volume', hue='Type')    
    # # plt.show()
    
    
def plt__line_graph(share_data_info_per_date):
    melted_df = share_data_info_per_date.melt(id_vars=['SYMBOL', 'Date'], var_name='Type', value_name='Volume')
    sns.lineplot(data=melted_df, x='Date', y='Volume', hue='Type', marker='o')
    plt.title('Aggregated Volume Over Time')
    plt.xlabel('Date')
    plt.ylabel('Volume')
    plt.show()    
    
list_of_files = []    
for x in os.listdir():
    if x.endswith(".csv"):   
        print("file being processed is: ", x)
        processed_file = process_file(x)
        list_of_files.append(processed_file)
       
# print(list_of_files)
All_share_data=pd.DataFrame(list_of_files,columns = ['Shares_Sold' , 'Shares_Bought', 'MATCH' , 'SYMBOL', 'Date','ToT_Volume_Traded',]) 
all_share_data=All_share_data.sort_values(by='Date')






    volume = row['Volume']
    print('m' in volume)
    if 'k' in volume:
        symbol_data['Volume'] = symbol_data['Volume'].str.replace('k', '')
        row['Volume'] = row['Volume'].replace(',', '').astype(float) * 1000
        print("worked")
    # Value = row['Value']    
    # if 'k' in Value:
    #     row['Value'] = row['Value'].replace('k', '')
    #     row['Value'] = row['Value'].replace(',', '').astype(float) * 1000   