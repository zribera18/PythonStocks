import bs4 as bs
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
import os
import pandas as pd
import pandas_datareader.data as web
import pickle
import requests

style.use('ggplot')

print 'hi'
non_sp500_watchlist = ["GME", "AMC", "APHA", "ACB", "AMD", "NIO"]

def save_sp500_tickers():
    resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text

        print(ticker.strip())
        tickers.append(ticker.strip())

    for ticker in non_sp500_watchlist:
        tickers.append(ticker.strip().decode('utf-8'))

    print(tickers)

    with open("sp500tickers.pickle", "wb") as f:
        pickle.dump(tickers, f)

    print tickers
    return tickers

# save_sp500_tickers()

def get_data_from_yahoo(reload_sp500=False):
    if reload_sp500:
        tickers = save_sp500_tickers()
    else:
        with open("sp500tickers.pickle", "rb") as f:
            tickers = pickle.load(f)

    if not os.path.exists('stock_dfs_2021'):
        os.mkdir('stock_dfs_2021')

    start = dt.datetime(2021, 1, 1)
    end = dt.datetime(2021, 12, 31)

    print('getting data from yahoo for dates {} through {}.'.format(str(start), str(end)))

    for ticker in tickers:
        print(ticker)
        if not os.path.exists('stock_dfs_2021/{}.csv'.format(ticker)):
            df = web.DataReader(ticker.replace('.','-'), 'yahoo', start, end)
            df.to_csv('stock_dfs_2021/{}.csv'.format(ticker))
            # df.set_index('Date', inplace=True)
        else:
            print('Already have {}'.format(ticker))

get_data_from_yahoo(reload_sp500=True)


def compile_data():
    with open("sp500tickers.pickle", "rb") as f:
        tickers = pickle.load(f)

    main_df = pd.DataFrame()

    for count, ticker in enumerate(tickers):
        df = pd.read_csv('stock_dfs_2021/{}.csv'. format(ticker))
        df.set_index('Date', inplace=True)

        df.rename(columns={'Adj Close': ticker}, inplace=True)
        df.drop(['Open','High', 'Low', 'Close','Volume'], 1, inplace=True)

        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df, how='outer')

        if count % 10 == 0:
            print(count)

    print(main_df.head())
    main_df.to_csv('sp500_joined_closes.csv')

compile_data()

# python for finance part 8
def vizualize_data():
    df = pd.read_csv('sp500_joined_closes.csv')
    # df['AAPL'].plot()
    # plt.show()
    df_corr = df.corr()

    print(df_corr.head())

    data = df_corr.values
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)

    heatmap = ax.pcolor(data, cmap=plt.cm.RdYlGn)

    fig.colorbar(heatmap)
    ax.set_xticks(np.arange(data.shape[0]) + 0.5, minor=False)
    ax.set_yticks(np.arange(data.shape[1]) + 0.5, minor=False)
    ax.invert_yaxis()
    ax.xaxis.tick_top()

    column_labels = df_corr.columns
    row_labels = df_corr.index

    ax.set_xticklabels(column_labels)
    ax.set_yticklabels(row_labels)
    plt.xticks(rotation=90)
    heatmap.set_clim(-1,1)

    plt.tight_layout()
    plt.show()

vizualize_data()
