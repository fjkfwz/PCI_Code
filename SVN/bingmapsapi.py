import json
from urllib import urlopen, quote_plus
import advancedclassify
bingkey = "AoAoiIYIxV6pWRN_nHSgYz2BGaYqhlDC63_FXHQCteUAI2VthrUo9lJN5P4Dx_6k"
loc_cache = {}


def loadnumerical():
    oldrows = advancedclassify.loadmatch('matchmaker.csv')
    newrows = []
    out = open('numerical.txt', 'w+')
    for row in oldrows:
        d = row.data
        data = [float(d[0]), advancedclassify.yesno(d[1]), advancedclassify.yesno(d[2]), advancedclassify.yesno(d[5]),
                advancedclassify.yesno(d[6]), advancedclassify.yesno(d[7]), advancedclassify.matchcount(d[3], d[8]),
                milesdistance(d[4], d[9]), row.match]
        newrows.append(advancedclassify.matchrow(data))
        print(advancedclassify.matchrow(data).__str__())
        out.write("%s\n" % data)
    out.close()
    return newrows


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


def milesdistance(a1, a2):
    lat1, long1 = getlocation(a1)
    print lat1, long1
    lat2, long2 = getlocation(a2)
    print lat2, long2
    latdif = 69.1 * (lat2 - lat1)
    longdif = 53.0 * (long2 - long1)
    return (latdif ** 2 + longdif ** 2) ** .5
