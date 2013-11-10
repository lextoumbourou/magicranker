import pandas as pd


def get_timestamps(price_data):
    return sorted(
        set([date for date in price_data['date']]))


def generate_buys_evenly(price_data, portfolio_size, symbols):
    buys = {}
    parcel_price = float(portfolio_size) / len(symbols)
    for symbol in symbols:
        price = price_data[price_data.index == symbol].close[0]
        buys[symbol] = parcel_price / price

    return buys


def simulate(price_data, buys, start_date, end_date):
    data = pd.DataFrame(index=get_timestamps(price_data))
    for symbol in buys:
        data[symbol] = buys[symbol] * price_data[
            price_data.index == symbol]['close'].values
        print data[symbol]

    data['total'] = 0
    for symbol in buys:
        data['total'] += data[symbol]

    return data
