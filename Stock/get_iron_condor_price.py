from datetime import date, datetime, timedelta
import nr2stock
import urllib
import sys
import re
import os.path
import pprint

# 5-ple = (name, low put, high put, low call, high call)
condors = [
  ('GOOGL',  '2014-08-29', 'RUT140822P01125000', 'RUT140822P01145000', 'RUT140822C01155000', 'RUT140822C01175000')
  ]

pp = pprint.PrettyPrinter(indent=4)
for c in condors:
  print c[0]
  pp.pprint(nr2stock.get_options_chain_values(c[0], c[1]))

