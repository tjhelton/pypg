# import os
import pandas as pd
# import requests

TOKEN = ''

def read_csv():
    df = pd.read_csv('input.csv')
    csv = df.to_dict('records')
    return csv
