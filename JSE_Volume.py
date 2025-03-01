import seaborn as sns
import os
import pandas as pd
import numpy as np
import re
from datetime import datetime
# Replace 'your_file.xlsx' with the path to your Excel file
#file_path = '/path/to/your_file.xlsx' 

def process_file(file_path):
    # Read the CSV file
   # file_path ='/Users/senzosenkosishezi/Desktop/JSE_Volume_Tracker/JSE_Volume_Tracker/Course of Sales (GRT.JSE)_2025-02-27T17_05_47+02_00.csv'
    JSE_symbol = re.search(r'\((.*?)\)', file_path)
    Date_trade_volume = re.search(r'\d{4}-\d{2}-\d{2}', file_path)
    symbol_data= pd.read_csv(file_path)
    
    # Replace empty strings with NaN
    symbol_data.replace(r'^\s*$', np.nan, regex=True, inplace=True)
    
    symbol_data.replace(r'^\s*$', np.nan, regex=True)
    symbol_data['Traded_Volume'] = symbol_data['Value'].replace('-', 'MATCH')
    # Replace '-' with 'MATCH' in 'Value' column
    
    
    symbol_data['Rand_Value'] = symbol_data['Volume'].str.split('  ', expand=True)
    symbol_data['Rand_Value']=symbol_data['Rand_Value'].astype(str)
    symbol_data['Rand_Value']=symbol_data['Rand_Value'].replace(',','',regex=True)
    symbol_data['Rand_Value']=symbol_data['Rand_Value'].astype(float)

    aggregated_volume = symbol_data.groupby('Traded_Volume')['Rand_Value'].sum()

    share_data_info_per_date= aggregated_volume.to_dict()
    #share_data_info_per_date.append(JSE_symbol.group(1))
    #share_data_info_per_date.append(Date_trade_volume.group())
    # final_Data = ['BID','ASK','MATCH']
    
    # dicti={'TOT_BID':0,'TOT_ASK':0,'MATCH':0,'SYMBOL':0,'Date':0}
    
    
    share_data_info_per_date['SYMBOL'] = JSE_symbol.group(1)
    share_data_info_per_date['Date'] = Date_trade_volume.group()
    share_data_info_per_date = pd.DataFrame([share_data_info_per_date])
    print(share_data_info_per_date)
for x in os.listdir():
    if x.endswith(".csv"):
        # Prints only text file present in My Folder
        #print(x)
        process_file(x)
        


