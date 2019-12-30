import bs4 as bs
import pickle
import requests


def save_sp500_tickers():
    resp = requests.get('')
    soup = bs.BeautifulSoup(resp.txt)

    table = soup.find('table', {'class':'wikitable sortable'})
    tickets = []

    for row in table.findAll('tr')[1:]:
        ticekr = row.findall('td')[0].text
        tickers.append(ticker)

    with open("sp500tickers.pickle","wb") as f:
        pickle.dimp(tickers, f)

    return tickers