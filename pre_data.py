import pandas as pd
import numpy as np
import os

data_path = './data/kdd17/raw/'
output_path = './data/kdd17/pred/'
start_date = '2017-07-03'
end_date = '2022-01-01'

class Features:
    def __init__(self, df, trading_dates):
        self.df = df
        self.trading_dates = trading_dates

    def c_feature(self, numerator, close):
        return (numerator / close - 1) * 100

    def n_feature(self, nclose, pclose):
        return (nclose / pclose - 1) * 100

    def days_feature(self, days, closes):
        return ((sum(close for close in closes) / days) / closes[-1] - 1) * 100

    def label(self, pt, pt1):
        move = pt1 / pt - 1
        if move >= 0.0055:
            return 1
        elif move <= -0.005:
            return -1
        else:
            return 0

    def gen(self):
        pred = pd.DataFrame(columns=['c_open', 'c_high', 'c_low', 'n_close', 'n_adj_close', '5day',\
                            '10day', '15day', '20day', '25day', '30day', 'label'])
        for date in self.trading_dates:
            if date in df.index.values:
                data = []
                open = df.loc[date]['Open']
                high = df.loc[date]['High']
                low = df.loc[date]['Low']
                closes = df[df.index.get_loc(date)-29:df.index.get_loc(date)+1]['Close']
                if closes.shape[0] == 0:
                    data = [-123321]*12
                    pred.loc[len(pred)] = data
                    continue
                adj_closes = df[df.index.get_loc(date)-29:df.index.get_loc(date)+1]['Adj Close']
                data.append(self.c_feature(open, closes[-1]))
                data.append(self.c_feature(high, closes[-1]))
                data.append(self.c_feature(low, closes[-1]))
                data.append(self.n_feature(closes[-1], closes[-2]))
                data.append(self.n_feature(adj_closes[-1], adj_closes[-2]))
                for i in [5, 10, 15, 20, 25, 30]:
                    data.append(self.days_feature(i, closes.tail(i)))
                data.append(self.label(adj_closes[-1], df.iloc[df.index.get_loc(date)+1]['Adj Close']))
                pred.loc[len(pred)] = data

            else:
                data = [-123321]*12
                pred.loc[len(pred)] = data

        return pred

if __name__ == '__main__':

    fnames = [fname for fname in os.listdir(data_path) if os.path.isfile(os.path.join(data_path, fname))]

    df = pd.read_csv(os.path.join(data_path, fnames[0]))
    df = df.loc[df['Date'].between(start_date, end_date)]
    trade_dates = df['Date']
    trade_dates.to_csv(output_path+'../trading_dates.csv', index=False, header=False)
    for fname in fnames:
        df = pd.read_csv(os.path.join(data_path, fname))
        df.set_index('Date', inplace=True)
        features = Features(df, trade_dates)
        # print(fname)
        output = features.gen()
        if type(output) is not bool:
            output.to_csv(os.path.join(output_path, fname), index=False, header=False)
