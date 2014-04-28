from datetime import date, datetime, timedelta
import urllib

def valid_market_date(check_date):
    # If we run into a market holiday, just go back a day until we're open
    if is_market_closed(check_date):
        return valid_market_date(check_date - timedelta(days=1))
    else:
        return check_date

def is_market_closed(check_date):
    close_dates  = {
        '2012-01-02': 1,
        '2012-01-16': 1,
        '2012-02-20': 1,
        '2012-04-06': 1,
        '2012-05-28': 1,
        '2012-07-04': 1,
        '2012-09-03': 1,
        '2012-11-22': 1,
        '2012-12-25': 1,
        '2013-01-01': 1,
        '2013-01-21': 1,
        '2013-02-18': 1,
        '2013-03-29': 1,
        '2013-05-27': 1,
        '2013-07-04': 1,
        '2013-09-02': 1,
        '2013-11-28': 1,
        '2013-12-25': 1,
        '2014-01-01': 1,
        '2014-01-20': 1,
        '2014-02-17': 1,
        '2014-04-18': 1,
        '2014-05-26': 1,
        '2014-07-04': 1,
        '2014-09-01': 1,
        '2014-11-27': 1,
        '2014-12-25': 1,
        }
    if check_date.weekday()==5 or check_date.weekday()==6 or check_date.strftime("%Y-%m-%d") in close_dates:
        return True
    else:
        return False

def get_historical_data(symbol, get_date=None):
    if get_date.strftime("%Y-%m-%d")==date.today().strftime("%Y-%m-%d") or get_date is None: # get current day
        # opening price, current price
        url = "http://finance.yahoo.com/d/quotes.csv?s=%s&f=ol1" % ( \
            symbol, \
            )
        u = urllib.urlopen(url)
        data = u.readline()
        arg_list = []
        for arg in data.split(','):
            arg_list.append(float(arg))
        return {
            'open': arg_list[0],
            'close': arg_list[1],
            }
    else:
        trading_period = 'd'
        # Output: Date,Open,High,Low,Close,Volume,Adj Close
        url = 'http://ichart.yahoo.com/table.csv?s=%s&a=%s&b=%s&c=%s&d=%s&e=%s&f=%s&g=%s&ignore=.csv' % ( \
            symbol, \
            get_date.month-1, \
            get_date.day, \
            get_date.year, \
            get_date.month-1, \
            get_date.day, \
            get_date.year, \
            trading_period, \
            )
        u = urllib.urlopen(url)
        u.readline()
        data = u.readline()
        arg_list = data.split(',')
        return {
            'open': float(arg_list[1]),
            'close': float(arg_list[2]),
            }

