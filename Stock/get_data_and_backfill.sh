#/bin/bash

START_DATE=2014-06-26
WRITE_FILE=current.csv
DATA_DIR=/Users/nrodrigo/git/Scripts/Stock/output

echo "Generating stock data for $START_DATE"
echo "Deleting data"
echo "delete from quotes where close_date>='$START_DATE';" | /usr/local/mysql/bin/mysql -u root stock

echo "Getting Stock Data"
/usr/bin/python get_stock_data.py start_date=$START_DATE write_to=$WRITE_FILE > /dev/null

echo "Loading data"
echo "load data local infile '$DATA_DIR/$WRITE_FILE' into table quotes fields terminated by ',' lines terminated by '\n' (symbol,close_date,open,high,low,close,volume,adj_close);" | /usr/local/mysql/bin/mysql -u root stock

echo "Backfill ETL"
/usr/local/mysql/bin/mysql -u root stock < backfill_previous_close.sql

echo "All done... good luck Mr. Trump"
