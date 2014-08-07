from datetime import date, datetime, timedelta
import nr2stock
import urllib
import sys
import re
import os.path

#
# Usage:
# python get_settlement_data.py start_date=2014-03-01 end_date=2014-04-01 write_to=weekly_settlement.2014-03.csv
# This will loop through until end_date.  end_date will not run.
#
# This will run a single day
# python get_settlement_data.py start_date=2014-03-01 write_to=weekly_settlement.2014-03-01.csv
#
# python get_settlement_data.py start_date=2014-05-01 write_to=current_settlement.csv
#

start_date = None
end_date = None
for arg in sys.argv:
    if re.match('^start_date', arg):
        start_date = arg.split('=')[1]
        if re.match('\d\d\d\d-\d\d-\d\d', start_date) is None:
            print "start_date must be in the format yyyy-mm-dd"
            sys.exit()
        else:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
    if re.match('^end_date', arg):
        end_date = arg.split('=')[1]
        if re.match('\d\d\d\d-\d\d-\d\d', end_date) is None:
            print "end_date must be in the format yyyy-mm-dd"
            sys.exit()
        else:
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
    if re.match('^write_to', arg):
        write_to = arg.split('=')[1]

if start_date is None:
    print "Must enter start_date\n"
    sys.exit()

if end_date is None:
    end_date = datetime.today() + timedelta(days=1)

data = []
i=1
get_date = start_date

write_file = "./output/"+write_to
file = open(write_file, "w")
symbol_list = nr2stock.settlement_list()
while get_date.date() < end_date.date():
    if nr2stock.is_market_closed(get_date):
        get_date += timedelta(days=1)
        continue
    for symbol in symbol_list:
        print "Processing %s %s" % (symbol, get_date.strftime("%Y-%m-%d"))
        #get_data = nr2stock.get_settlement_values(symbol, get_date)
        get_data = nr2stock.get_settlement_values(symbol)
        if get_data is None:
            continue
            
        string =  "%s,%s,%s,%s,%s,%s,%s,%s\n" \
            % (symbol, get_data['date'], get_data['open'], get_data['high'], get_data['low'], get_data['close'], get_data['volume'], get_data['adj_close'])
        file.write(string)
    get_date += timedelta(days=1)
file.close()

