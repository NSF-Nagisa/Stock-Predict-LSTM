import pandas as pd
import os

data_path = './data/acl18/pred/'

for file in os.listdir(data_path):
    df = pd.read_csv(data_path+file)
    df.drop(df.columns[[-1]], axis=1, inplace=True)
    df.to_csv(data_path+file, index=False)