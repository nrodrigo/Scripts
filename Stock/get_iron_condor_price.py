from datetime import date, datetime, timedelta
import nr2stock
import urllib
import sys
import re
import os.path

# 5-ple = (name, low put, high put, low call, high call)
condors = [
  ('RUT 22 AUG 14', 'RUT140822P01125000', 'RUT140822P01145000', 'RUT140822C01155000', 'RUT140822C01175000')
  ]

for c in condors:
  print c[0]
  nr2stock.get_options_chain_values(c[1])

