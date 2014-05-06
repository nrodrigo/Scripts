import nr2stock
import sys

symbol_list = nr2stock.symbol_list()

for symbol in symbol_list:
    strike_interval = nr2stock.get_strike_interval(symbol)
    # These are strikes that YQL doesn't supply
    if symbol == '^RUT':
        print "update symbol_type set strike_interval = 10.0 where symbol='%s';" % (strike_interval, symbol)
    elif symbol == 'XRO' or symbol == '^NDX' or symbol == '^OEX':
        print "update symbol_type set strike_interval = 5.0 where symbol='%s';" % (strike_interval, symbol)
    elif strike_interval is not None:
        print "update symbol_type set strike_interval = %s where symbol='%s';" % (strike_interval, symbol)
