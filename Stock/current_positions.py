import nr2stock
import MySQLdb
import sys

"""
insert into current_positions set
  symbol = 'ARCB',
  price_at_purchase = '38.82',
  low_call = 'BTO Jun 14 38 Call',
  high_call = 'STO Jun 14 42 Call',
  outlook = 'bull',
  type = 'debit',
  low_strike = '38.00',
  high_strike = '42.00',
  low_fill = '3.30',
  high_fill = '1.30',
  qty = 1,
  status = 'current'
  ;
"""

db = MySQLdb.connect(host="localhost", user="root", db="stock")
cur = db.cursor()
cur.execute("select * from current_positions where status='current' order by symbol")
num_fields = len(cur.description)
field_names = [i[0] for i in cur.description]
print ""
total_gain = 0.00
total_actual_gain = 0.00
total_loss = 0.00
check_date = nr2stock.most_recent_market_date()

for row in cur.fetchall():
    i = 0
    quote = {}
    for var in row:
        quote[field_names[i]] = var
        i=i+1

    low_strike = float(quote['low_strike'])
    high_strike = float(quote['high_strike'])
    low_fill = float(quote['low_fill'])
    high_fill = float(quote['high_fill'])
    qty = float(quote['qty'])
    price_at_purchase = float(quote['price_at_purchase'])

    print "Symbol: %s, %s @ $%s (%s %s)" % (quote['symbol'], int(qty), "%.2f" % price_at_purchase, quote['outlook'], quote['type'])
    print "Low/High Option: %s @ $%s / %s @ $%s" % (quote['low_call'], "%.2f" % low_fill, quote['high_call'], "%.2f" % high_fill)

    debit_credit = 0.00
    stock_data = nr2stock.get_historical_data_all(quote['symbol'], check_date)
    current = float(stock_data['close'])
    print "Current: $%s" % ("%.2f" % current)
    if quote['outlook']=='bull':
        debit_credit = (quote['high_fill']-quote['low_fill'])*100
    elif quote['outlook']=='bear':
        debit_credit = (quote['low_fill']-quote['high_fill'])*100
    debit_credit = float(debit_credit) * qty
    print "Debit(-)/Credit(+): $%s" % ("%.2f" % debit_credit)

    actual_gain = 0.00
    max_gain = 0.00
    max_loss = 0.00
    if quote['type']=='credit':
        max_gain = debit_credit
        max_loss = ((high_strike-low_strike)*100*qty)-debit_credit
        if quote['outlook']=='bull':
            actual_gain = nr2stock.calc_gain_loss('long put', low_strike, current, low_fill) + \
                nr2stock.calc_gain_loss('short put', high_strike, current, high_fill)
        else:
            actual_gain = nr2stock.calc_gain_loss('short call', low_strike, current, low_fill) + \
                nr2stock.calc_gain_loss('long call', high_strike, current, high_fill)
    else:
        max_gain = ((high_strike-low_strike)*100)+debit_credit
        max_loss = -1*debit_credit
        if quote['outlook']=='bull':
            actual_gain = nr2stock.calc_gain_loss('long call', low_strike, current, low_fill) + \
                nr2stock.calc_gain_loss('short call', high_strike, current, high_fill)
        else:
            actual_gain = nr2stock.calc_gain_loss('short put', low_strike, current, low_fill) + \
                nr2stock.calc_gain_loss('long call', high_strike, current, high_fill)
    actual_gain = actual_gain*qty
    if (actual_gain<0):
        alert = "(!!!)"
    else:
        alert = ""
    print "Max Potential Gain/Loss/Risk: $%s / $%s / %s%%" % ("%.2f" % max_gain, "%.2f" % max_loss, "%.2f" % ((max_gain/max_loss)*100))
    print "Actual Gain: $%s %s" % ("%.2f" % actual_gain, alert)
    total_gain = float(total_gain) + float(max_gain)
    total_actual_gain = float(total_actual_gain) + float(actual_gain)
    total_loss = float(total_loss) + float(max_loss)

    print ""

print "Total Potential Gain: $%s" % ("%.2f" % total_gain)
print "Total Potential Loss: $%s" % ("%.2f" % total_loss)
print "Total Potential Risk: %s%%" % ("%.2f" % ((total_gain/total_loss)*100))
print ""
print "Total Acutal Gain: $%s" % ("%.2f" % total_actual_gain)
print "Total Actual Risk: %s%%" % ("%.2f" % ((total_actual_gain/total_loss)*100))

