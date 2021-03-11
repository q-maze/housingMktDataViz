import pandas as pd

def get_data():
    df = pd.read_csv('https://opendata.arcgis.com/datasets/8eaa0b89826244ae9246915199462328_0.csv')
    return df
