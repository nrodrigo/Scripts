from datetime import date, datetime, timedelta
import nr2stock
import urllib
import sys
import re
import os.path

#
# Usage:
# python weekly_options.py start_date={yyyy-mm-ff}
#  if no date given, it will use current day
#  if no week_range given, will scan 1, 2, 3 and 4 weeks
#
# Example:
#  python weekly_options.py start_date=2013-01-01
#

start_date = None
for arg in sys.argv:
    if re.match('^start_date', arg):
        start_date = arg.split('=')[1]
        if re.match('\d\d\d\d-\d\d-\d\d', start_date) is None:
            print "start_date must be in the format yyyy-mm-dd"
            sys.exit()
        else:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')

# key -> value
# key is the way the symbol appears on CBOE's site
# value is the way we retrieve it from Yahoo finance
symbol_list = {
    'OEX': '^OEX',
    'XEO': 'XEO',
    'SPX': '^GSPC',
    ##'DJX': '^DJX',
    'NDX': '^NDX',
    'RUT': '^RUT',
    'AGQ': 'AGQ',
    'DIA': 'DIA',
    'DUST': 'DUST',
    'DXJ': 'DXJ',
    'EEM': 'EEM',
    'EFA': 'EFA',
    'EPI': 'EPI',
    'EWJ': 'EWJ',
    'EWW': 'EWW',
    'EWZ': 'EWZ',
    'FAS': 'FAS',
    'FAZ': 'FAZ',
    'FXE': 'FXE',
    'FXI': 'FXI',
    'FXY': 'FXY',
    'GDXJ': 'GDXJ',
    'GLD': 'GLD',
    ##'GLD7': 'GLD7',
    'GDX': 'GDX',
    'HYG': 'HYG',
    'IWM': 'IWM',
    'IYR': 'IYR',
    'ITB': 'ITB',
    'QQQ': 'QQQ',
    'MDY': 'MDY',
    'NUGT': 'NUGT',
    'OIH': 'OIH',
    'SCO': 'SCO',
    'SDS': 'SDS',
    'SLV': 'SLV',
    'SPY': 'SPY',
    ##'SPY7': 'SPY7',
    'SSO': 'SSO',
    'SVXY': 'SVXY',
    'TBT': 'TBT',
    'TLT': 'TLT',
    'TNA': 'TNA',
    'TZA': 'TZA',
    'UCO': 'UCO',
    'USO': 'USO',
    'UNG': 'UNG',
    'UUP': 'UUP',
    'UVXY': 'UVXY',
    'VWO': 'VWO',
    'VXX': 'VXX',
    'XHB': 'XHB',
    'XLB': 'XLB',
    'XLE': 'XLE',
    'XLF': 'XLF',
    'XLI': 'XLI',
    'XLK': 'XLK',
    'XLP': 'XLP',
    'XLU': 'XLU',
    'XLV': 'XLV',
    'XLY': 'XLY',
    'XME': 'XME',
    'XOP': 'XOP',
    'XRT': 'XRT',
    'AA': 'AA',
    'AAL': 'AAL',
    'AAPL': 'AAPL',
    ##'AAPL7': 'AAPL7',
    'ABT': 'ABT',
    'ABX': 'ABX',
    'ACN': 'ACN',
    'ADM': 'ADM',
    'AET': 'AET',
    'AFSI': 'AFSI',
    'AGNC': 'AGNC',
    'AGU': 'AGU',
    'AIG': 'AIG',
    'AKAM': 'AKAM',
    'AKS': 'AKS',
    'ALXN': 'ALXN',
    'AMD': 'AMD',
    'AMGN': 'AMGN',
    'AMRN': 'AMRN',
    'AMT': 'AMT',
    'AMZN': 'AMZN',
    ##'AMZN7': 'AMZN7',
    'ANF': 'ANF',
    'ANR': 'ANR',
    'AOL': 'AOL',
    'APA': 'APA',
    'APC': 'APC',
    'APOL': 'APOL',
    'ARIA': 'ARIA',
    'ARNA': 'ARNA',
    'ATHN': 'ATHN',
    'ATVI': 'ATVI',
    'AVP': 'AVP',
    'AXP': 'AXP',
    'BA': 'BA',
    'BAC': 'BAC',
    'BAX': 'BAX',
    'BBBY': 'BBBY',
    'BBRY': 'BBRY',
    'BBY': 'BBY',
    'BHI': 'BHI',
    'BIDU': 'BIDU',
    'BIIB': 'BIIB',
    'BK': 'BK',
    'BMY': 'BMY',
    'BP': 'BP',
    'BRCM': 'BRCM',
    'BTU': 'BTU',
    'BX': 'BX',
    'C': 'C',
    'CAT': 'CAT',
    'CBS': 'CBS',
    'CELG': 'CELG',
    'CF': 'CF',
    'CHK': 'CHK',
    'CL': 'CL',
    'CLF': 'CLF',
    'CMCSA': 'CMCSA',
    'CMG': 'CMG',
    'CME': 'CME',
    'CMI': 'CMI',
    'COF': 'COF',
    'COH': 'COH',
    'COP': 'COP',
    'COST': 'COST',
    'CSCO': 'CSCO',
    'CREE': 'CREE',
    'CRM': 'CRM',
    'CRUS': 'CRUS',
    'CTRP': 'CTRP',
    'CTSH': 'CTSH',
    'CVX': 'CVX',
    'CZR': 'CZR',
    'DAL': 'DAL',
    'DD': 'DD',
    'DDD': 'DDD',
    'DE': 'DE',
    'DECK': 'DECK',
    'DG': 'DG',
    'DHI': 'DHI',
    'DIS': 'DIS',
    'DISH': 'DISH',
    'DNDN': 'DNDN',
    'DOW': 'DOW',
    'DRYS': 'DRYS',
    'DVN': 'DVN',
    'EA': 'EA',
    'EBAY': 'EBAY',
    #'ELN': 'ELN',
    'EMC': 'EMC',
    'EOG': 'EOG',
    'EQIX': 'EQIX',
    'ESRX': 'ESRX',
    'ETFC': 'ETFC',
    'ETN': 'ETN',
    'EXPE': 'EXPE',
    'EXXI': 'EXXI',
    'F': 'F',
    'FB': 'FB',
    'FCX': 'FCX',
    'FDO': 'FDO',
    'FDX': 'FDX',
    #'FEYE': 'FEYE',
    'FFIV': 'FFIV',
    'FLR': 'FLR',
    'FOSL': 'FOSL',
    'FSLR': 'FSLR',
    'GALE': 'GALE',
    'GE': 'GE',
    'GG': 'GG',
    'GILD': 'GILD',
    'GLW': 'GLW',
    'GM': 'GM',
    'GMCR': 'GMCR',
    'GME': 'GME',
    'GNW': 'GNW',
    'GOOGL': 'GOOGL',
    #'GOOG': 'GOOG',
    'GPS': 'GPS',
    'GRPN': 'GRPN',
    'GS': 'GS',
    'GT': 'GT',
    'HAL': 'HAL',
    'HCA': 'HCA',
    'HD': 'HD',
    'HES': 'HES',
    'HFC': 'HFC',
    'HLF': 'HLF',
    'HON': 'HON',
    'HPQ': 'HPQ',
    'HUM': 'HUM',
    'IBM': 'IBM',
    'ICPT': 'ICPT',
    'INTC': 'INTC',
    'INVN': 'INVN',
    'IOC': 'IOC',
    'IP': 'IP',
    'ISRG': 'ISRG',
    'JCP': 'JCP',
    'JNJ': 'JNJ',
    'JNPR': 'JNPR',
    'JOY': 'JOY',
    'JPM': 'JPM',
    'KBH': 'KBH',
    'KGC': 'KGC',
    'KMB': 'KMB',
    'KO': 'KO',
    'KORS': 'KORS',
    'KSS': 'KSS',
    #'LCC': 'LCC',
    'LINE': 'LINE',
    'LLY': 'LLY',
    'LNG': 'LNG',
    'LNKD': 'LNKD',
    'LOW': 'LOW',
    'LULU': 'LULU',
    'LVS': 'LVS',
    'M': 'M',
    'MA': 'MA',
    'MBI': 'MBI',
    'MCD': 'MCD',
    'MCP': 'MCP',
    'MDLZ': 'MDLZ',
    'MDT': 'MDT',
    'MET': 'MET',
    'MGM': 'MGM',
    'MMM': 'MMM',
    'MNKD': 'MNKD',
    'MNST': 'MNST',
    'MO': 'MO',
    'MON': 'MON',
    'MOS': 'MOS',
    'MPC': 'MPC',
    'MPEL': 'MPEL',
    'MRK': 'MRK',
    'MRO': 'MRO',
    'MRVL': 'MRVL',
    'MS': 'MS',
    'MSFT': 'MSFT',
    'MTG': 'MTG',
    'MU': 'MU',
    'MYGN': 'MYGN',
    'NAV': 'NAV',
    'NBG': 'NBG',
    'NE': 'NE',
    'NEM': 'NEM',
    'NFLX': 'NFLX',
    'NKE': 'NKE',
    'NLY': 'NLY',
    'NOK': 'NOK',
    'NOV': 'NOV',
    'NTAP': 'NTAP',
    'NUE': 'NUE',
    'NUS': 'NUS',
    'NVDA': 'NVDA',
    'ORCL': 'ORCL',
    'OXY': 'OXY',
    'P': 'P',
    'PANW': 'PANW',
    'PBR': 'PBR',
    'PCLN': 'PCLN',
    'PCYC': 'PCYC',
    'PFE': 'PFE',
    'PG': 'PG',
    'PHM': 'PHM',
    'PLUG': 'PLUG',
    'PM': 'PM',
    'POT': 'POT',
    'PSX': 'PSX',
    'QCOM': 'QCOM',
    'QCOR': 'QCOR',
    'QIHU': 'QIHU',
    'QLIK': 'QLIK',
    'RAD': 'RAD',
    'RAX': 'RAX',
    'REGN': 'REGN',
    'S': 'S',
    'SBUX': 'SBUX',
    'SCTY': 'SCTY',
    'SDRL': 'SDRL',
    'SINA': 'SINA',
    'SIRI': 'SIRI',
    'SLB': 'SLB',
    'SLW': 'SLW',
    'SNDK': 'SNDK',
    'SNE': 'SNE',
    'SODA': 'SODA',
    'SPWR': 'SPWR',
    'SRPT': 'SRPT',
    'SSYS': 'SSYS',
    'STX': 'STX',
    'SU': 'SU',
    'SUNE': 'SUNE',
    'SWKS': 'SWKS',
    'SWY': 'SWY',
    'SYY': 'SYY',
    'T': 'T',
    'TAP': 'TAP',
    'TGT': 'TGT',
    'TIF': 'TIF',
    'TIVO': 'TIVO',
    'TMUS': 'TMUS',
    'TOL': 'TOL',
    'TRIP': 'TRIP',
    'TSLA': 'TSLA',
    'TSO': 'TSO',
    'TTM': 'TTM',
    ##'TWTR': 'TWTR',
    'TXN': 'TXN',
    'UA': 'UA',
    'UNH': 'UNH',
    'UNP': 'UNP',
    'UNXL': 'UNXL',
    'UPS': 'UPS',
    'USB': 'USB',
    'UTX': 'UTX',
    'V': 'V',
    'VALE': 'VALE',
    'VHC': 'VHC',
    'VLO': 'VLO',
    'VMW': 'VMW',
    'VOD': 'VOD',
    'VRTX': 'VRTX',
    'VVUS': 'VVUS',
    'VZ': 'VZ',
    'WAG': 'WAG',
    'WDC': 'WDC',
    'WFC': 'WFC',
    'WFM': 'WFM',
    'WFT': 'WFT',
    'WLP': 'WLP',
    'WLT': 'WLT',
    'WMB': 'WMB',
    'WMT': 'WMT',
    'WYNN': 'WYNN',
    'X': 'X',
    'XOM': 'XOM',
    'YELP': 'YELP',
    'YHOO': 'YHOO',
    'YNDX': 'YNDX',
    'YUM': 'YUM',
    'Z': 'Z',
    'ZNGA': 'ZNGA',
    #'ZTS': 'ZTS',
}

symbol_order = (
    'OEX',
    'XEO',
    'SPX',
    'DJX',
    'NDX',
    'RUT',
    'AGQ',
    'DIA',
    'DUST',
    'DXJ',
    'EEM',
    'EFA',
    'EPI',
    'EWJ',
    'EWW',
    'EWZ',
    'FAS',
    'FAZ',
    'FXE',
    'FXI',
    'FXY',
    'GDXJ',
    'GLD',
    'GLD7',
    'GDX',
    'HYG',
    'IWM',
    'IYR',
    'ITB',
    'QQQ',
    'MDY',
    'NUGT',
    'OIH',
    'SCO',
    'SDS',
    'SLV',
    'SPY',
    'SPY7',
    'SSO',
    'SVXY',
    'TBT',
    'TLT',
    'TNA',
    'TZA',
    'UCO',
    'USO',
    'UNG',
    'UUP',
    'UVXY',
    'VWO',
    'VXX',
    'XHB',
    'XLB',
    'XLE',
    'XLF',
    'XLI',
    'XLK',
    'XLP',
    'XLU',
    'XLV',
    'XLY',
    'XME',
    'XOP',
    'XRT',
    'AA',
    'AAL',
    'AAPL',
    'AAPL7',
    'ABT',
    'ABX',
    'ACN',
    'ADM',
    'AET',
    'AFSI',
    'AGNC',
    'AGU',
    'AIG',
    'AKAM',
    'AKS',
    'ALXN',
    'AMD',
    'AMGN',
    'AMRN',
    'AMT',
    'AMZN',
    'AMZN7',
    'ANF',
    'ANR',
    'AOL',
    'APA',
    'APC',
    'APOL',
    'ARIA',
    'ARNA',
    'ATHN',
    'ATVI',
    'AVP',
    'AXP',
    'BA',
    'BAC',
    'BAX',
    'BBBY',
    'BBRY',
    'BBY',
    'BHI',
    'BIDU',
    'BIIB',
    'BK',
    'BMY',
    'BP',
    'BRCM',
    'BTU',
    'BX',
    'C',
    'CAT',
    'CBS',
    'CELG',
    'CF',
    'CHK',
    'CL',
    'CLF',
    'CMCSA',
    'CMG',
    'CME',
    'CMI',
    'COF',
    'COH',
    'COP',
    'COST',
    'CSCO',
    'CREE',
    'CRM',
    'CRUS',
    'CTRP',
    'CTSH',
    'CVX',
    'CZR',
    'DAL',
    'DD',
    'DDD',
    'DE',
    'DECK',
    'DG',
    'DHI',
    'DIS',
    'DISH',
    'DNDN',
    'DOW',
    'DRYS',
    'DVN',
    'EA',
    'EBAY',
    'ELN',
    'EMC',
    'EOG',
    'EQIX',
    'ESRX',
    'ETFC',
    'ETN',
    'EXPE',
    'EXXI',
    'F',
    'FB',
    'FCX',
    'FDO',
    'FDX',
    'FEYE',
    'FFIV',
    'FLR',
    'FOSL',
    'FSLR',
    'GALE',
    'GE',
    'GG',
    'GILD',
    'GLW',
    'GM',
    'GMCR',
    'GME',
    'GNW',
    'GOOGL',
    'GOOG',
    'GPS',
    'GRPN',
    'GS',
    'GT',
    'HAL',
    'HCA',
    'HD',
    'HES',
    'HFC',
    'HLF',
    'HON',
    'HPQ',
    'HUM',
    'IBM',
    'ICPT',
    'INTC',
    'INVN',
    'IOC',
    'IP',
    'ISRG',
    'JCP',
    'JNJ',
    'JNPR',
    'JOY',
    'JPM',
    'KBH',
    'KGC',
    'KMB',
    'KO',
    'KORS',
    'KSS',
    'LCC',
    'LINE',
    'LLY',
    'LNG',
    'LNKD',
    'LOW',
    'LULU',
    'LVS',
    'M',
    'MA',
    'MBI',
    'MCD',
    'MCP',
    'MDLZ',
    'MDT',
    'MET',
    'MGM',
    'MMM',
    'MNKD',
    'MNST',
    'MO',
    'MON',
    'MOS',
    'MPC',
    'MPEL',
    'MRK',
    'MRO',
    'MRVL',
    'MS',
    'MSFT',
    'MTG',
    'MU',
    'MYGN',
    'NAV',
    'NBG',
    'NE',
    'NEM',
    'NFLX',
    'NKE',
    'NLY',
    'NOK',
    'NOV',
    'NTAP',
    'NUE',
    'NUS',
    'NVDA',
    'ORCL',
    'OXY',
    'P',
    'PANW',
    'PBR',
    'PCLN',
    'PCYC',
    'PFE',
    'PG',
    'PHM',
    'PLUG',
    'PM',
    'POT',
    'PSX',
    'QCOM',
    'QCOR',
    'QIHU',
    'QLIK',
    'RAD',
    'RAX',
    'REGN',
    'S',
    'SBUX',
    'SCTY',
    'SDRL',
    'SINA',
    'SIRI',
    'SLB',
    'SLW',
    'SNDK',
    'SNE',
    'SODA',
    'SPWR',
    'SRPT',
    'SSYS',
    'STX',
    'SU',
    'SUNE',
    'SWKS',
    'SWY',
    'SYY',
    'T',
    'TAP',
    'TGT',
    'TIF',
    'TIVO',
    'TMUS',
    'TOL',
    'TRIP',
    'TSLA',
    'TSO',
    'TTM',
    'TWTR',
    'TXN',
    'UA',
    'UNH',
    'UNP',
    'UNXL',
    'UPS',
    'USB',
    'UTX',
    'V',
    'VALE',
    'VHC',
    'VLO',
    'VMW',
    'VOD',
    'VRTX',
    'VVUS',
    'VZ',
    'WAG',
    'WDC',
    'WFC',
    'WFM',
    'WFT',
    'WLP',
    'WLT',
    'WMB',
    'WMT',
    'WYNN',
    'X',
    'XOM',
    'YELP',
    'YHOO',
    'YNDX',
    'YUM',
    'Z',
    'ZNGA',
    'ZTS',
);

data = []
i=1
get_date = start_date

while get_date.date() < datetime.today().date():
    for symbol in symbol_order:
        if symbol_list.get(symbol, None) is None:
            continue
        if nr2stock.is_market_closed(get_date):
            get_date += timedelta(days=1)
            continue

        print "Processing %s %s" % (symbol_list.get(symbol, None), get_date.strftime("%Y-%m-%d"))

        get_data = nr2stock.get_historical_data_all(symbol_list[symbol], get_date)
        write_file = "./output/weekly.sql"
        file = open(write_file, "w")
        insert_string =  "insert into quotes set symbol='%s', close_date='%s', open='%s', high='%s', low='%s', close='%s', volume='%s', adj_close='%s';" \
            % (symbol_list[symbol], get_data['date'], get_data['open'], get_data['high'], get_data['low'], get_data['close'], get_data['volume'], get_data['adj_close'])
        file.write(insert_string)
    get_date += timedelta(days=1)


# filename:
#   output_(date_of_markettrend_list)_(date_report_run)_(timestamp).csv
#write_file = "./output/output_%s_%s_%s.csv" % (markettrend_date, start_date.strftime("%Y%m%d"), datetime.now().strftime("%Y%m%d%H%M%S"))
#file = open(write_file, "w")
#file.write(','.join(headers)+"\n")
#for row in data:
#    get_row = []
#    for header in headers:
#        get_row.append(str(row[header]))
#    file.write(','.join(get_row)+"\n")
#file.close()