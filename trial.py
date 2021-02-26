import pandas as pd

path = 'E:/B.Tech Project/NHSTA_ACCELERATION_DATA/front.csv'
data_csv = pd.read_csv(path)
x = data_csv['t']

print(x)