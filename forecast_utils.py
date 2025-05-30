import pandas as pd

def preprocess_data(df):
    df = df.copy()
    df = df.dropna()
    df = df.sort_index()
    return df

def split_data(df):
    train_df = df.iloc[:148]
    test_df = df.iloc[148:156]
    return train_df, test_df
