import json
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import datetime

def extract_data():
    
    with open(file_name, 'r') as f:
        lines = json.load(f)
        
    df_data = pd.DataFrame(lines['animals'][0]['time_series'])
    
    return df_data

def transform_data(extracted_data):
    
    extracted_data['timestamp'] = pd.to_datetime(extracted_data['timestamp'], format='%Y-%m-%d %H:%M:%S')
    extracted_data.replace('NA', method = 'pad', inplace = True)
    extracted_data = extracted_data.set_index('timestamp')
    
    # Nao necessario para o teste
    cast_list = list(extracted_data.loc[:, extracted_data.dtypes == object].columns)
    extracted_data[cast_list] = extracted_data[cast_list].astype(np.int64)
    
    aux_data = extracted_data[['rumination', 'activity']]
    transformed_data = aux_data.groupby(pd.Grouper(freq = 'D')).sum()
    
    return transformed_data

def exp_smooth(df_data, alpha):
    
    delta = datetime.timedelta(days = 1)
    
    flag = True
    
    for i, row in df_data.iterrows():
        if flag:
            df_data.loc[i, 'exp_smooth'] = row['activity']
            flag = False
        else:
            df_data.loc[i, 'exp_smooth'] = alpha * row['activity'] + (1 - alpha) * df_data.loc[i - delta, 'exp_smooth']
    
    return df_data

def main():
    
    extracted_data = extract_data()
    transformed_data = transform_data(extracted_data)
    exp_smoothed_data = exp_smooth(transformed_data, alpha = 0.05)