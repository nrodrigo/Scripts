from datetime import date, datetime, timedelta
import nr2stock
import urllib
import sys
import re
import os.path

#
#
# This script returns averages across all markettrendsignal musclestock
#
# Usage:
# python get_averages.py data_file=output_20140303_20140304_20140304163229.csv
#
#

data_file = None
for arg in sys.argv:
    if re.match('^data_file', arg):
        data_file = arg.split('=')[1]
        if os.path.isfile('./output/%s'%(data_file))==False:
            print "File doesn't exists: ./output/%s" % (data_file)
            sys.exit()
        else:
            data_file = './output/%s'%(data_file)

if data_file is None:
    print "Must supply an data_file (see output directory)"
    sys.exit()

file = open(data_file, 'r')
headers = []
field_array = {}
results = {}
for line in file:
    data = line.rstrip('\n').split(',')
    if len(headers)==0:
        i = 0
        for var in data:
            if re.search('pctincr', var):
                results[var] = []
                field_array[i] = var
                headers.append(var)
            i = i+1
    else:
        i = 0
        for var in data:
            if i in field_array:
                results[field_array[i]].append(float(var))
            i = i+1

file.close()

for week in sorted(results.keys()):
    print "%s: %s" % (week, sum(results[week])/float(len(results[week])))
