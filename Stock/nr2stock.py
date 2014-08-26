from datetime import date, datetime, timedelta
import urllib
import sys
import re
import datetime
import yql
import httplib
import urllib
try: import simplejson as json
except ImportError: import json

def valid_market_date(check_date):
    # If we run into a market holiday, just go back a day until we're open
    if is_market_closed(check_date):
        return valid_market_date(check_date - timedelta(days=1))
    else:
        return check_date

def is_market_closed(check_date):
    close_dates  = {
        '2011-01-17': 1,
        '2011-02-21': 1,
        '2011-04-22': 1,
        '2011-05-30': 1,
        '2011-07-04': 1,
        '2011-09-05': 1,
        '2011-11-24': 1,
        '2011-11-25': 1,
        '2011-12-26': 1,
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

def most_recent_market_date():
    days_back = 0
    while (1):
        get_date = date.today() - timedelta(days_back)
        if is_market_closed(get_date):
            days_back += 1
        else:
            break
    return get_date
        

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
        # Per http://www.jarloo.com/get-historical-stock-data/:
        #   Output: Date,Open,High,Low,Close,Volume,Adj Close
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
        print arg_list
        return {
            'open': float(arg_list[1]),
            'close': float(arg_list[2]),
            }


def get_historical_data_all(symbol, get_date=None):
    if get_date.strftime("%Y-%m-%d")==date.today().strftime("%Y-%m-%d") or get_date is None: # get current day
        # opening price, current price
        url = "http://finance.yahoo.com/d/quotes.csv?s=%s&f=ol1hgv" % ( \
            symbol, \
            )
        u = urllib.urlopen(url)
        data = u.readline()
        arg_list = []
        for arg in data.split(','):
            if arg=='N/A':
                return None
            arg_list.append(float(arg))
        return {
            'date': date.today().strftime("%Y-%m-%d"),
            'open': '%.2f' % float(arg_list[0]),
            'close': '%.2f' % float(arg_list[1]),
            'high': '%.2f' % float(arg_list[2]),
            'low': '%.2f' % float(arg_list[3]),
            'volume': int(arg_list[4]),
            'adj_close': '%.2f' % float(arg_list[1]),
            }
    else:
        trading_period = 'd'
        # Per http://www.jarloo.com/get-historical-stock-data/:
        #   Output: Date,Open,High,Low,Close,Volume,Adj Close
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
        if re.search( r'404 Not Found', data):
            print 'symbol not found %s' % (symbol)
            print url
            return None
            #sys.exit()

        arg_list = data.split(',')

        return {
            'date': str(arg_list[0]),
            'open': '%.2f' % float(arg_list[1]),
            'high': '%.2f' % float(arg_list[2]),
            'low': '%.2f' % float(arg_list[3]),
            'close': '%.2f' % float(arg_list[4]),
            'volume': int(arg_list[5]),
            'adj_close': '%.2f' % float(arg_list[6]),
            }

def symbol_list():
    file = open("./symbol_list.txt", "r")
    ret = []
    for symbol in file.read().split("\n"):
        if symbol and re.match('^#', symbol) is None:
            ret.append(symbol)
    return ret

def settlement_list():
    file = open("./settlement_list.txt", "r")
    ret = []
    for symbol in file.read().split("\n"):
        if symbol and re.match('^#', symbol) is None:
            ret.append(symbol)
    return ret

#def get_options_chain(symbol):
def get_strike_interval(symbol):

    PUBLIC_API_URL = 'http://query.yahooapis.com/v1/public/yql'
    DATATABLES_URL = 'store://datatables.org/alltableswithkeys'

    yql = 'select * from yahoo.finance.options where symbol = \'%s\'' \
          % (symbol)

    conn = httplib.HTTPConnection('query.yahooapis.com')
    queryString = urllib.urlencode({'q': yql, 'format': 'json', 'env': DATATABLES_URL})
    conn.request('GET', PUBLIC_API_URL + '?' + queryString)
    obj = json.loads(conn.getresponse().read())

    try:
        get_option_chain = obj['query']['results']['optionsChain']['option']
    except KeyError:
        return None
    except TypeError:
        return None

    get_strikes = {}


    for x in get_option_chain:
        strike_price = float(x['strikePrice'])
        if strike_price not in get_strikes:
            get_strikes[strike_price] = 0
        get_strikes[strike_price] += 1
    interval = 0
    prev = 0
    i = 0
    for x in reversed(sorted(get_strikes.keys())):
        if prev==0:
            prev = x
        else:
            interval = interval + (prev-x)
            prev = x
        i = i+1
    return float("%.1f" % (interval/i))

def calc_gain_loss(option_type, strike_price, current, fill_price):
    cur_gain_loss = 0.00
    if option_type=='long call':
        if current <= strike_price:
            cur_gain_loss = fill_price*100*-1
        else:
            cur_gain_loss = (current-strike_price-fill_price)*100
    elif option_type=='long put':
        if current >= strike_price:
            cur_gain_loss = fill_price*100*-1
        else:
            cur_gain_loss = (strike_price-current-fill_price)*100
    elif option_type=='short call':
        if current <= strike_price:
            cur_gain_loss = fill_price*100
        else:
            cur_gain_loss = (strike_price-current+fill_price)*100
    elif option_type=='short put':
        if current >= strike_price:
            cur_gain_loss = fill_price*100
        else:
            cur_gain_loss = (current-strike_price-fill_price)*100
    return cur_gain_loss


def get_settlement_values(symbol):

    PUBLIC_API_URL = 'http://query.yahooapis.com/v1/public/yql'
    DATATABLES_URL = 'store://datatables.org/alltableswithkeys'

    #yql = 'select * from yahoo.finance.quotes where symbol = \'%s\'' \
    #      % (symbol)
    yql = 'select * from yahoo.finance.quotes where symbol = \'%s\' and date>=\'2014-05-01\' ' \
          % (symbol)

    conn = httplib.HTTPConnection('query.yahooapis.com')
    queryString = urllib.urlencode({'q': yql, 'format': 'json', 'env': DATATABLES_URL})
    conn.request('GET', PUBLIC_API_URL + '?' + queryString)
    obj = json.loads(conn.getresponse().read())

    print obj
    #try:
    #    get_option_chain = obj['query']['results']['optionsChain']['option']
    #except KeyError:
    #    return None
    #except TypeError:
    #    return None

    return 1

def get_options_chain_values(symbol, expiration_date):

    PUBLIC_API_URL = 'http://query.yahooapis.com/v1/public/yql'
    DATATABLES_URL = 'store://datatables.org/alltableswithkeys'

    yql = 'select * from yahoo.finance.options where symbol=\'%s\' and expiration=\'%s\'' % (symbol, expiration_date)
    #yql = 'select * from yahoo.finance.options where symbol=\'RUT\' and expiration=\'2014-08\'' # % (symbol)

    conn = httplib.HTTPConnection('query.yahooapis.com')
    queryString = urllib.urlencode({'q': yql, 'format': 'json', 'env': DATATABLES_URL})
    conn.request('GET', PUBLIC_API_URL + '?' + queryString)
    obj = json.loads(conn.getresponse().read())

    return obj
    #try:
    #    get_option_chain = obj['query']['results']['optionsChain']['option']
    #except KeyError:
    #    return None
    #except TypeError:
    #    return None

    return 1
