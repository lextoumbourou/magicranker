from magicranker.stock.models import PriceHistory

def get_price_data(stocks, start_date, end_date):
    """ Return a pandas dataframe with price data for a list of stocks

    args:
        stocks - list of stock symbols 
        start_date - datetime object
        end_date - datetime object

    return:
        pandas.core.frame.DataFrame
    """
    data = PriceHistory.objects.filter(
        code__code__in=stocks, date__gte=start_date, date__lte=end_date)

    return data.to_dataframe(index='code', coerce_float=True)
