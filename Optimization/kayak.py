import time
import urllib2
import xml.dom.minidom
import json

api_key = ""
ts_code = ""


def getkeyaksession():
    data = {"trips": [
        {
            "departure_code": "SYD",
            "arrival_code": "LON",
            "outbound_date": "2014-01-24",
            "inbound_date": "2014-01-29"
        }], "adults_count": 1
    }
    url = 'api.wego.com/flights/api/k/2/searches?api_key=%s&ts_code=%s' % (api_key, ts_code)
    req = urllib2.Request(url)
    req.add_header('Content-Type', 'application/json')
    req.add_header('Accept', 'application/json')
    doc = xml.dom.minidom.parseString(urllib2.urlopen(req, json.dumps(data)).read())
    sid = doc.getElementsByTagName('sid')[0].firstChild.data
    return sid


def flightsearch(origin, destination, depart_date):
    data = {"trips": [{
        "departure_code": '%s',
        "arrival_code": '%s',
        "outbound_date": '%s',
        "inbound_date": "2014-01-29"
    }] % (origin, destination, depart_date)}
    url = 'api.wego.com/flights/api/k/2/searches?api_key=%s&ts_code=%s' % (api_key, ts_code)
    req = urllib2.Request(url)
    req.add_header('Content-Type', 'application/json')
    req.add_header('Accept', 'application/json')
    doc = xml.dom.minidom.parseString(urllib2.urlopen(req, json.dumps(data)).read())
    print url
    doc = xml.dom.minidom.parseString(urllib2.urlopen(url).read())
    searchid = doc.getElementsByTagName('searchid')[0].firstChild.data
    return searchid


def flightsearchresults(searchid):
    def parseprice(p):
        return float(p[1:].replace(',', ''))

    data = {"id": "1376967853520",
            "search_id": "%s",
            "trip_id": "SYD:LON:2014-01-24:2014-01-29",
            "fares_query_type": "route",
            "sort": "price",
            "order": "asc",
            "page": 1,
            "per_page": 10,
            "currency_code": "EUR",
            "price_min_usd": 515,
            "price_max_usd": 1700,
            "departure_day_time_filter_type": "separate",
            "stop_types": ["none"],
            "provider_codes": ["expedia.com", "farebuzz.com"],
            "aiport_codes": ["LCY", "LHR"],
            "airline_codes": ["SQ", "CZ"],
            "designator_codes": ["SQ221", "CZ301"],
            "duration_max": 2090,
            "duration_min": 300,
            "outbound_departure_day_time_min": 360,
            "outbound_departure_day_time_max": 1300,
            "inbound_departure_day_time_min": 400,
            "inbound_departure_day_time_max": 1200
            }
    while 1:
        time.sleep(2)
        url = 'api.wego.com/flights/api/k/2/searches?api_key=%s&ts_code=%s' % (api_key, ts_code)
        req = urllib2.Request(url)
        req.add_header('Content-Type', 'application/json')
        req.add_header('Accept', 'application/json')
        doc = xml.dom.minidom.parseString(urllib2.urlopen(req, json.dumps(data)).read())
        morepending = doc.getElementsByTagName('morepending')[0].firstChild
        if morepending == None or morepending.data == 'false': break
    prices = doc.getElementsByTagName('price')
    departure = doc.getElementsByTagName('depart')
    arrivals = doc.getElementsByTagName('arrive')

    return zip([p.firstChild.data.spilt(' ')[1] for p in departure],
               [p.firstChild.data.spilt(' ')[1] for p in arrivals],
               [p.firstChild.data.spilt(' ')[1] for p in prices])


def createschedule(people, dest, dep, ret):
    sid = getkeyaksession()
    flights = {}
    for p in people:
        name, origin = p
        searchid = flightsearch(origin, dest, dep)
        flights[(dest, origin)] = flightsearchresults(searchid)
    return flights
