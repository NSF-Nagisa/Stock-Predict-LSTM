import requests
import os 
import pandas as pd

input_path = '../Adv-ALSTM/data/kdd17/price_long_50'
output_path = './data/kdd17/raw/'
start = '2017-01-01'
end = '2022-05-01'

fnames = [fname for fname in os.listdir(input_path) if
              os.path.isfile(os.path.join(input_path, fname))]

def build_url(ticker, start_date = start, end_date = end, interval = '1d'):
    base_url = 'https://query1.finance.yahoo.com/v8/finance/chart/'
    end_seconds = int(pd.Timestamp(end_date).timestamp())
    start_seconds = int(pd.Timestamp(start_date).timestamp())
    site = base_url + ticker
    params = {'period1': start_seconds, 'period2': end_seconds, 'interval': interval.lower(), 'events': 'div,splits'}

    return site, params

def get_data(ticker, start_date = start, end_date = end, interval = '1d',
            headers = {'User-Agent': 'Mozilla/5.0'}):
    site, params = build_url(ticker, start_date, end_date, interval)
    print(site, params)
    res = requests.get(site, params=params, headers=headers)
    data = res.json()
    print(data)

    df = pd.DataFrame(data['chart']['result'][0]['indicators']['quote'][0])

    temp_time = data['chart']['result'][0]['timestamp']

    df['adjclose'] = data['chart']['result'][0]['indicators']['adjclose'][0]['adjclose']
    df.index = pd.to_datetime(temp_time, unit='s')
    df.index = df.index.map(lambda dt : dt.floor('d'))
    df = df(['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])

    return df

for fname in fnames:
    stock_name = fname.split('.')[0]
    data = get_data(stock_name)
    data.to_csv(os.path.join(output_path, fname))