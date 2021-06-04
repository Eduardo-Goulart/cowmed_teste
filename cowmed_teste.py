import json
import pandas as pd
import numpy as np
import datetime
from generate_plots import generate_plots

def extract_data():
    
    file_name = 'P2.json'
    
    with open(file_name, 'r') as input_file:
        raw_data = json.load(input_file)
        
    extracted_data = pd.DataFrame(raw_data['animals'][0]['time_series'])
    
    cow_id = raw_data['animals'][0]['earring']

    return extracted_data, cow_id

def transform_data(extracted_data):
    
    extracted_data['timestamp'] = pd.to_datetime(extracted_data['timestamp'], format='%Y-%m-%d %H:%M:%S')
    extracted_data.set_index('timestamp', inplace = True)
    
    transformed_data = extracted_data[['rumination', 'activity']].rolling(24).sum().dropna()
        
    return transformed_data

def create_alert(row):
    
    if row['activity'] - row['rumination'] > 200:
        return True
    else:
        return False

def exponential_smooth_data(transformed_data, alpha):

    time_delta = datetime.timedelta(hours = 1)
    
    flag = True

    for i, row in transformed_data.iterrows():    
        
        if flag:
            transformed_data.loc[i, 'exp_smooth'] = row['activity']
            flag = False
        else:
            transformed_data.loc[i, 'exp_smooth'] = alpha * row['activity'] + \
                                                    (1 - alpha) * transformed_data.loc[i - time_delta, 'exp_smooth']
        
        transformed_data.loc[i, 'alert'] = create_alert(row)
            
    return transformed_data

def calculate_residue(smoothed_data):
    
    smoothed_data['residue'] = smoothed_data['activity'] - smoothed_data['exp_smooth']
    
    return smoothed_data

def main():
    
    extracted_data, cow_id = extract_data()
    
    print(f'generating report for cow_id: {cow_id}')
    
    transformed_data = transform_data(extracted_data)
    smoothed_data = exponential_smooth_data(transformed_data, alpha = 0.05)
    processed_data = calculate_residue(smoothed_data)
    generate_plots(processed_data, cow_id)
        
main()