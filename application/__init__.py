from flask import Flask, request, Response, json
import numpy as np
import pandas as pd
import requests
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

#load data
#create flask instance

#create 
def get_historical_data(symbol, start_date = None):
    api_key = open(r'api_key.txt')
    api_url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={api_key}&outputsize=full'
    raw_df = requests.get(api_url).json()
    df = pd.DataFrame(raw_df[f'Time Series (Daily)']).T
    df = df.rename(columns = {'1. open': 'open', '2. high': 'high', '3. low': 'low', '4. close': 'close', '5. adjusted close': 'adj close', '6. volume': 'volume'})
    for i in df.columns:
        df[i] = df[i].astype(float)
    df.index = pd.to_datetime(df.index)
    df = df.iloc[::-1].drop(['7. dividend amount', '8. split coefficient'], axis = 1)
    if start_date:
        df = df[df.index >= start_date]
    return df

app = Flask(__name__)

@app.route('/api', methods=['GET', 'POST'])
def predict():
    #get data from request
    data = request.get_json(force=True)
    df = get_historical_data(data['ticker'], "2019-01-01")
    average = np.average(df['open'])
    #median = np.median(df['open'])
    #stdev = np.std(df['open'])
    print(df)
    return Response(json.dumps(average))

