import datetime as dt

import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt
from matplotlib import style

style.use('ggplot')

# start = dt.datetime(2000,1,1)
#
# end = dt.datetime(2016,1, 1)
#
# df = web.DataReader('TSLA', 'yahoo', start, end)
# df.to_csv('tsla.csv')
df = pd.read_csv('tsla.csv', parse_dates=True, index_col=0)

df_ohlc = df['Adj Close'].resample('10D').ohlc()
df_volume = df['Volume'].resample('10D').sum()

df_ohlc.reset_index(inplace=True)
print(df_ohlc.head())

df_ohlc['Date'] = df_ohlc['Date'].map(_ + "Hi")

print(df_ohlc.head())


# df['100ma'] = df['Adj Close'].rolling(window = 100, min_periods=0).mean()
# df.(inplace=True)

# print(df.head(10))

# ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
# ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)
#
# plt.show()

# print(df[['Open', 'High']].head())

# df['Adj Close'].plot()
# plt.show()



