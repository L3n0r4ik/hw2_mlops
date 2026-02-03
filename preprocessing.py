import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')

def preprocess(df):
    df = df.copy()
    
    df['transaction_time'] = pd.to_datetime(df['transaction_time'])
    df['transaction_hour'] = df['transaction_time'].dt.hour
    df['transaction_day'] = df['transaction_time'].dt.day
    df['transaction_month'] = df['transaction_time'].dt.month
    df['transaction_weekday'] = df['transaction_time'].dt.weekday
    
    categorical_features = ['merch', 'cat_id', 'gender', 'us_state', 'one_city']
    
    df['distance'] = np.sqrt(
        (df['lat'] - df['merchant_lat'])**2 + (df['lon'] - df['merchant_lon'])**2
    )
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if df[col].isnull().any():
            df[col] = df[col].fillna(df[col].median())
    
    cat_cols = df.select_dtypes(include=['object']).columns
    for col in cat_cols:
        if df[col].isnull().any():
            df[col] = df[col].fillna('missing')
    
    return df