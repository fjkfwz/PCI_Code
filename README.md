# PCI_Code
《集体智慧编程》(Programming Collective Intelligence)源代码

##fix bugs
###修复原书过期API
1.将原书第9章：SVN Yahoo API替换方法为bingMaps API:http://dev.virtualearth.net/
```
def getlocation(address):
    if address in loc_cache: return loc_cache[address]
    url = 'http://dev.virtualearth.net/REST/v1/Locations?CountryRegion=US&addressLine=%s&maxResults=1&key=%s' % (
        quote_plus(address), bingkey)
    print url
    while True:
        data = urlopen(url).read()
        data_string = json.loads(data)
        print data_string['statusCode']
        if (data_string['statusCode'] == 200 and data_string['resourceSets'][0]['estimatedTotal'] == 1): break
    lat = data_string['resourceSets'][0]['resources'][0]['geocodePoints'][0]['coordinates'][0]
    long = data_string['resourceSets'][0]['resources'][0]['geocodePoints'][0]['coordinates'][1]
    loc_cache[address] = (float(lat), float(long))
    return loc_cache[address]
```
2.将原书第9章：KNM Yahoo API替换方法为新的Yahoo API :http://query.yahooapis.com/v1/public/yql
```
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
```
###增强代码健壮性
```
while True:
        rows = urlopen(
            "http://query.yahooapis.com/v1/public/yql?q= select * from yahoo.finance.historicaldata where symbol= \"%s\" and startDate = \"2012-09-11\" and endDate = \"2014-02-11\" &format=json &diagnostics=true &env=store://datatables.org/alltableswithkeys &callback=" % t).read()
        try:
            row_string = json.loads(rows)
        except:
            continue
        if (len(row_string["query"]["results"]["quote"]) > 0): break
  ```
