import seaborn as sns
import os
import pandas as pd
import numpy as np
import re
from datetime import datetime
import datetime as dt
import matplotlib.pyplot as plt


file_path='/Users/senzosenkosishezi/Desktop/JSE_Volume_Tracker/JSE_Volume_Tracker/Time Series (GND.JSE)_2025-03-01T22_32_02+02_00.csv'
#file_path ='/Users/senzosenkosishezi/Desktop/JSE_Volume_Tracker/JSE_Volume_Tracker/Course of Sales (GRT.JSE)_2025-02-27T17_05_47+02_00.csv'
JSE_symbol = re.search(r'\((.*?)\)', file_path)
Date_trade_volume = re.search(r'\d{4}-\d{2}-\d{2}', file_path)
cols=['Date','Open','High',	'Low','Close','Volume','Value','MktVWAP','Transactions','Adj. Factor']
symbol_data= pd.read_csv(file_path,skiprows=0,usecols=cols)

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
    
    

plt.figure(
    figsize=(8, 4),  # Set the figure size here
    dpi=100,  # Set the dpi (or resolution) here
)
list_ordering = ["Less than 1M", "1M to 5M", "5M to 10M", "10M to 100M", "More than 100M"]
symbol_data["Value_group"] = symbol_data["Value_group"].astype("category", categories=list_ordering, ordered=True)
# Create a horizontal barplot
sns.barplot(
    data=symbol_data,  # Specify the data to use
    x="Value_group",  # Set the variable for the length of the bars
    y="Value",  # Set the categorical variable on the y-axis
    ci=False,  # Turn of confidence intervals
    hue="Value_group",  # Set the variable to split by
)
plt.show()
    
plt.plot(symbol_data['Value'], label='Volume', color='blue')   
plt.title('GND.JSE Traded Volume Over Time')
plt.xlabel('Date')
plt.ylabel('Volume Traded')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6) # Add a grid for easier reading
    
plt.tight_layout() #prevents labels from being cut off
plt.show() 
 

 
    
    
# print(symbol_data['Value_group'].unique())
# # symbol_data=symbol_data.where(symbol_data['Date'] > '10-Feb-25')
# #print(symbol_data['Date'].to_timestamp())
# # symbol_data['Date'] = pd.to_datetime(symbol_data['Date'])  
# filter=symbol_data['year'] > 2023
# filter1=symbol_data['week'] > '2024-12-24'
# sns.scatterplot(data=symbol_data.where(filter1), x="Date", y="Value", hue="Value_group")

# # sns.barplot(symbol_data, x="Value_group", y="week",errorbar=None)
# #sns.lineplot(symbol_data.where(filter1), x="Date", y="Value", hue="Value_group")
# # sns.relplot(
# # data=symbol_data.where(filter), x="week", y="Value_group",
# # size="Value_group", sizes=(15, 200)
# # )
# plt.show()

