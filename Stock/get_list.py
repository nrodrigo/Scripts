from datetime import date, datetime, timedelta
import nr2stock
import urllib
import sys
import re
import os.path

#
# Usage:
# python get_list.py start_date={yyyy-mm-ff} week_range={x}
#  if no date given, it will use current day
#  if no week_range given, will scan 1, 2, 3 and 4 weeks
#
# Example:
#  python get_list.py input_file=muscle_stock_20140303.csv start_date=2014-03-03
#

start_date = None
week_range = None
input_file = None
for arg in sys.argv:
    if re.match('^start_date', arg):
        start_date = arg.split('=')[1]
        if re.match('\d\d\d\d-\d\d-\d\d', start_date) is None:
            print "start_date must be in the format yyyy-mm-dd"
            sys.exit()
        else:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
    elif re.match('^week_range', arg):
        week_range = arg.split('=')[1]
        try:
            week_range = int(week_range)
        except ValueError:
            print "week_range must be a number"
            sys.exit()
        week_range = [week_range]
    elif re.match('^input_file', arg):
        input_file = arg.split('=')[1]
        if os.path.isfile('./input/%s'%(input_file))==False:
            print "File doesn't exists: ./input/%s" % (input_file)
            sys.exit()
        else:
            input_file = './input/%s'%(input_file)

# input file must have a timestamp
markettrend_date = None
try:
    markettrend_date = re.search('\d\d\d\d\d\d\d\d', input_file).group(0)
except AttributeError:
    print "Need markettrend date"
    sys.exit()

if input_file is None:
    print "Must supply an input_file"
    sys.exit()
if start_date is None:
    start_date = date.today()
if week_range is None:
    week_range = [1, 2, 3, 4, 5, 6, 7, 8]

# at some point, we need to check if any date we check doesn't fall on a market open day
week_range_dates = {}
for week_ago in week_range:
    target_date = start_date - timedelta(weeks=week_ago)
    week_range_dates[week_ago] = nr2stock.valid_market_date(target_date)

file = open(input_file, 'r')
symbol_list = []
for line in file:
    line.rstrip('\n')
    symbol_list.append(line.rstrip('\n'))

# create headers
headers = ['symbol']
for week_ago in week_range:
    headers.append("weeks_ago_%s_open_%s"%(week_ago, week_range_dates[week_ago].strftime("%Y%m%d")))
headers.append("current_close_%s"%(start_date.strftime("%Y%m%d")))
for week_ago in week_range:
    target_date = start_date - timedelta(weeks=week_ago)
    headers.append("weeks_ago_%s_pctincr_%s"%(week_ago, week_range_dates[week_ago].strftime("%Y%m%d")))

data = []
i=1
for symbol in symbol_list:
    print "Retrieving data for %s (%s of %s)" % (symbol, i, str(len(symbol_list)+1))
    close_data = nr2stock.get_historical_data(symbol, start_date)
    header_data = {
        'symbol': symbol,
        "current_close_%s"%(start_date.strftime("%Y%m%d")): close_data['close']
        }
    for week_ago in week_range:
        hist_data = nr2stock.get_historical_data(symbol, week_range_dates[week_ago])
        header_data["weeks_ago_%s_open_%s"%(week_ago, week_range_dates[week_ago].strftime("%Y%m%d"))] = hist_data['open']
        header_data["weeks_ago_%s_pctincr_%s"%(week_ago, week_range_dates[week_ago].strftime("%Y%m%d"))] = (close_data['close']/hist_data['open'])-1;
    data.append(header_data)
    i = i+1

# filename:
#   output_(date_of_markettrend_list)_(date_report_run)_(timestamp).csv
write_file = "./output/output_%s_%s_%s.csv" % (markettrend_date, start_date.strftime("%Y%m%d"), datetime.now().strftime("%Y%m%d%H%M%S"))
file = open(write_file, "w")
file.write(','.join(headers)+"\n")
for row in data:
    get_row = []
    for header in headers:
        get_row.append(str(row[header]))
    file.write(','.join(get_row)+"\n")
file.close()
