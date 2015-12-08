import kayak

sid = kayak.getkeyaksession()
searchid = kayak.flightsearch(sid, 'BOS', 'LGA', '11/17/2014')
f = kayak.flightsearchresults(sid, searchid)
print f[0:3]
