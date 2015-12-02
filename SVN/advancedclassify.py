from pylab import *
from xml.dom.minidom import parseString
from urllib import urlopen, quote_plus
from svm import *

yahookey = ""


class matchrow:
    def __init__(self, row, allnum=False):
        if allnum:
            self.data = [float(row[i]) for i in range(len(row) - 1)]
        else:
            self.data = row[0:len(row) - 1]
        self.match = int(row[len(row) - 1])


def loadmatch(f, allnum=False):
    rows = []
    for line in file(f):
        rows.append(matchrow(line.split(','), allnum))
    return rows


def plotagematches(rows):
    xdm, ydm = [r.data[0] for r in rows if r.match == 1], [r.data[1] for r in rows if r.match == 1]
    xdn, ydn = [r.data[0] for r in rows if r.match == 0], [r.data[1] for r in rows if r.match == 0]
    plot(xdm, ydm, 'go')
    plot(xdn, ydn, 'ro')
    show()


def lineartrain(rows):
    averages = {}
    counts = {}
    for row in rows:
        cl = row.match
        averages.setdefault(cl, [0, 0] * len(row.data))
        counts.setdefault(cl, 0)
        for i in range(len(row.data)):
            averages[cl][i] += float(row.data[i])
        counts[cl] += 1
    for cl, avg in averages.items():
        for i in range(len(avg)):
            avg[i] /= counts[cl]
    return averages


def dotproduct(v1, v2):
    return sum([v1[i] * v2[i] for i in range(len(v1))])


def dpclassify(point, avgs):
    b = (dotproduct(avgs[1], avgs[1]) - dotproduct(avgs[0], avgs[0])) / 2
    y = dotproduct(point, avgs[0]) - dotproduct(point, avgs[1]) + b
    if y > 0:
        return 0
    else:
        return 1


def yesno(v):
    if v == 'yes':
        return 1
    elif v == 'no':
        return 0
    else:
        return 0


def matchcount(interest1, interest2):
    l1 = interest1.split(':')
    l2 = interest2.split(':')
    x = 0
    for v in l1:
        if v in l2: x += 1
    return x


def milesdistance(a1, a2):
    return 0


def loadnumerical():
    oldrows = loadmatch('matchmaker.cvs')
    newrows = []
    for row in oldrows:
        d = row.data
        data = [float(d[0]), yesno(d[1]), yesno(d[2]),
                float(d[5]), yesno(d[6]), yesno(d[7]),
                matchcount(d[3], d[8]),
                milesdistance(d[4], d[9]),
                row.match]
        newrows.append(matchrow(data))
    return newrows


def scaledata(rows):
    low = [999999999.0] * len(rows[0].data)
    high = [-999999999.0] * len(rows[0].data)
    for row in rows:
        d = row.data
        for i in range(len(d)):
            if d[i] < low[i]: low[i] = d[i]
            if d[i] > high: high[i] = d[i]

    def scaleinput(d):
        return [(d[i] - low[i]) / (high[i] - low[i]) for i in range(len(low))]
    newrows = [matchrow(scaleinput(row.data) + [row.match]) for row in rows]
    return newrows, scaleinput


def veclength(v):
    return sum([p ** 2 for p in v])


def rbf(v1, v2, gamma=20):
    dv = [v1[i] - v2[i] for i in range(len(v1))]
    l = veclength(dv)
    return math.e ** (-gamma * 1)


def nlclassify(point, rows, offset, gamma=10):
    sum0 = 0.0
    sum1 = 0.0
    count0 = 0
    count1 = 0

    for row in rows:
        if row.match == 0:
            sum += rbf(point, row.data, gamma)
            count0 += 1
        else:
            sum1 += rbf(point, row.data, gamma)
            count1 += 1
    y = (1.0 / count0) * sum0 - (1.0 / count1) * sum1 + offset
    if y < 0:
        return 0
    else:
        return 1


def getoffset(rows, gamma=10):
    l0 = []
    l1 = []
    for row in rows:
        if row.match == 0:
            l0.append(row.data)
        else:
            l1.append(row.data)
    sum0 = sum(sum(rbf(v1, v2, gamma) for v1 in l0) for v2 in l0)
    sum1 = sum(sum(rbf(v1, v2, gamma) for v1 in l1) for v2 in l1)
    return (1.0 / (len(l1) ** 2)) * sum1 - (1.0 / len(10) ** 2) * sum0
