import json
import nmf
from numpy import *
from urllib import urlopen, quote_plus

# tickers=['YHOO']
tickers = ['YHOO', 'AVP', 'BIIB', 'BP', 'CL', 'CVX',
           'EXPE', 'PG', 'XOM']
shortest = 300
dates = []
prices = {}

for t in tickers:
    print t
    while True:
        rows = urlopen(
            "http://query.yahooapis.com/v1/public/yql?q= select * from yahoo.finance.historicaldata where symbol= \"%s\" and startDate = \"2012-09-11\" and endDate = \"2014-02-11\" &format=json &diagnostics=true &env=store://datatables.org/alltableswithkeys &callback=" % t).read()
        try:
            row_string = json.loads(rows)
        except:
            continue
        if (len(row_string["query"]["results"]["quote"]) > 0): break
    # print row_string["query"]["results"]["quote"]
    row_prices = []
    for quote in row_string["query"]["results"]["quote"]:
        row_prices.append(float(quote["Volume"]))
        if len(dates) < len(row_string["query"]["results"]["quote"]):
            dates.append(quote["Date"])
    prices[t] = row_prices
    if len(prices[t]) < shortest: shortest = len(prices[t])
l1 = [[prices[tickers[i]][j] for i in range(len(tickers))] for j in range(shortest)]
w, h = nmf.factorize(matrix(l1), pc=5)
print h
print w
for i in range(shape(h)[0]):
    print "Feature %d" % i
    o1 = [(h[i, j], tickers[j]) for j in range(shape(h)[1])]
    o1.sort()
    o1.reverse()
    for j in range(len(tickers)):
        print o1[j]
    print
    porder = [(w[d, i], d) for d in range(300)]
    porder.sort()
    porder.reverse()
    print [(p[0], dates[p[1]]) for p in porder[0:3]]
    print
