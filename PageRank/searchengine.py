import urllib2
from BeautifulSoup import *
from urlparse import urljoin
import sqlite3 as sqlite

ignorewords = set(['the', 'of', 'to', 'and', 'a', 'in', 'is', 'it'])


class crawler:
    def __init__(self, dbname):
        self.con = sqlite.connect(dbname)

    def __del__(self):
        self.con.close()

    def dbcommit(self):
        self.con.commit()

    def getentryid(self, table, field, value, createnew=True):
        cur = self.con.execute(
            "select rowid from %s where %s='%s'" % (table, field, value))
        res = cur.fetchone()
        if res == None:
            cur = self.con.execute("insert into %s (%s) values ('%s')" % (table, field, value))
            return cur.lastrowid
        else:
            return res[0]

    def addtoindex(self, url, soup):
        if self.isindexed(url):
            return
        print 'Indexing %s' % url
        text = self.gettextonly(soup)
        words = self.sparatewords(text)

        urlid = self.getentryid('urllist', 'url', url)

        for i in range(len(words)):
            word = words[i]
            if word in ignorewords: continue
            wordid = self.getentryid('wordlist', 'word', word)
            self.con.execute("insert into wordlocation(urlid,wordid,location) values (%d,%d,%d)" % (urlid, wordid, i))

    def gettextonly(self, soup):
        return None

    def sparatewords(self, text):
        return None

    def isindexed(self, url):
        u = self.con.execute(
            "select rowid from urllist where url='%s'" % url).fetchone()
        if u != None:
            v = self.con.execute(
                'select * from wordlocation where urlid= %d' % u[0]).fetchone()
            if v != None: return True
        return False

    def addlinkref(self, urlFrom, urlTo, linkText):
        words = self.sparatewords(linkText)
        fromid = self.getentryid('urllist', 'url', urlFrom)
        toid = self.getentryid('urllist', 'url', urlTo)
        if fromid == toid: return
        cur = self.con.execute("insert into link(fromid,toid) values (%d,%d)" % (fromid, toid))
        linkid = cur.lastrowid
        for word in words:
            if word in ignorewords: continue
            wordid = self.getentryid('wordlist', 'word', word)
            self.con.execute("insert into linkword(linkid,wordid) values (%d,%d)" % (linkid, wordid))

    def createindextables(self):
        self.con.execute('CREATE TABLE urllist(url)')
        self.con.execute('CREATE TABLE wordlist(word)')
        self.con.execute('CREATE TABLE wordlocation(urlid, wordid, location)')
        self.con.execute('CREATE TABLE link(fromid INTEGER, toid INTEGER)')
        self.con.execute('CREATE TABLE linkword(wordid, linkid)')
        self.con.execute('CREATE INDEX wordidx ON wordlist(word)')
        self.con.execute('CREATE INDEX urlidx ON urllist(url)')
        self.con.execute('CREATE INDEX wordurlidx ON wordlocation(wordid)')
        self.con.execute('CREATE INDEX urltoidx ON link(toid)')
        self.con.execute('CREATE INDEX urlfromidx ON link(fromid)')
        self.dbcommit()

    def crawl(self, pages, depth=2):
        for i in range(depth):
            newpages = set()
            for page in pages:
                print(page)
                try:
                    c = urllib2.urlopen(page)
                except:
                    print 'Failed to Open Url: %s' % page
                    continue
                soup = BeautifulSoup(c.read())
                self.addtoindex(page, soup)
                links = soup('a')
                for link in links:
                    if ('href' in dict(link.attrs)):
                        url = urljoin(page, link['href'])
                        if url.find("'") != -1: continue
                        url = url.split('#')[0]
                        if url[0:4] == 'http' and not self.isindexed(url):
                            newpages.add(url)
                        linkText = self.gettextonly(link)
                        self.addlinkref(page, url, linkText)
            self.dbcommit()
            pages = newpages

    def gettextonly(self, soup):
        v = soup.string
        if v == None:
            c = soup.contents
            resulttext = ''
            for t in c:
                subtext = self.gettextonly(t)
                resulttext += subtext + '/n'
            return resulttext
        else:
            return v.strip()

    def sparatewords(self, text):
        splitter = re.compile('\\W*')
        return [s.lower() for s in splitter.split(text) if s != '']

    def caculatepagerank(self, interation=20):
        self.con.execute('DROP TABLE IF EXISTS pagerank')
        self.con.execute('CREATE TABLE pagerank(urlid PRIMARY KEY, score)')
        self.con.execute('INSERT INTO pagerank SELECT ROWID ,1.0 FROM urllist')
        self.dbcommit()
        for i in range(interation):
            print "Iteration %d" % (i)
            for (urlid,) in self.con.execute('SELECT ROWID FROM  urllist'):
                pr = 0.15
                for (linker,) in self.con.execute(
                                "SELECT distinct fromid FROM link WHERE toid = %d" % urlid):
                    linkingpr = self.con.execute("SELECT score FROM pagerank WHERE urlid = %d" % linker).fetchone()[0]
                    linkingcount = self.con.execute(
                        "SELECT count(*) FROM link WHERE fromid= %d" % linker).fetchone()[0]
                    pr += 0.85 * (linkingpr / linkingcount)
                    self.con.execute(
                        "UPDATE pagerank set score=%f WHERE urlid=%d" % (pr, urlid))
                    self.dbcommit()


class search:
    def __init__(self, dbname):
        self.con = sqlite.connect(dbname)

    def __del__(self):
        self.con.close()

    def getmatchros(self, q):
        fieldlist = 'w0.urlid'
        tablelist = ''
        clauselist = ''
        wordids = []
        words = q.split(' ')
        tablenumber = 0

        for word in words:
            wordrow = self.con.execute(
                "select rowid from wordlist where word='%s'" % word).fetchone()
            if wordrow != None:
                wordid = wordrow[0]
                wordids.append(wordid)
                if tablenumber > 0:
                    tablelist += ','
                    clauselist += ' and '
                    clauselist += 'w%d.urlid=w%d.urlid and ' % (tablenumber - 1, tablenumber)
                fieldlist += ',w%d.location' % tablenumber
                tablelist += 'wordlocation w%d' % tablenumber
                clauselist += 'w%d.wordid=%d' % (tablenumber, wordid)
                tablenumber += 1
        if (fieldlist != None and tablelist != None and clauselist != None):
            fullquery = 'select %s from %s where %s' % (fieldlist, tablelist, clauselist)
            cur = self.con.execute(fullquery)
            rows = [row for row in cur]
        return rows, wordids

    def getscoredlist(self, rows, wordlist):
        totalscores = dict([(row[0], 0) for row in rows])
        # weights = [(1.0, self.frequencyscore(rows))]
        # weights = [(1.0, self.distancescore(rows))]
        weights = [(1.0, self.frequencyscore(rows)), (1.0, self.distancescore(rows)), (1.0, self.pagerankscore(rows))]
        for (weight, scores) in weights:
            for url in totalscores:
                totalscores[url] += weight * scores[url]
        return totalscores

    def geturlname(self, id):
        return self.con.execute("select url from urllist where rowid=%d" % id).fetchone()[0]

    def query(self, q):
        rows, wordids = self.getmatchros(q)
        scores = self.getscoredlist(rows, wordids)
        rankedscores = sorted([(score, url) for (url, score) in scores.items()], reverse=1)
        for (score, url) in rankedscores[0:10]:
            print "%f\t%s" % (score, self.geturlname(url))

    def normalizescores(self, scores, smallIsBetter=0):
        vsmall = 0.00001
        if smallIsBetter:
            minscore = min(scores.values())
            return dict([(u, float(minscore) / max(vsmall, l)) for (u, l) in scores.items()])
        else:
            maxscore = max(scores.values())
            if maxscore == 0: maxscore = vsmall
            return dict([(u, float(c) / maxscore) for (u, c) in scores.items()])

    def frequencyscore(self, rows):
        counts = dict([(row[0], 0) for row in rows])
        for row in rows:
            counts[row[0]] += 1
        return self.normalizescores(counts)

    def distancescore(self, rows):
        # If there's only one word, everyone wins!
        if len(rows[0]) <= 2: return dict([(row[0], 1.0) for row in rows])

        # Initialize the dictionary with large values
        mindistance = dict([(row[0], 1000000) for row in rows])

        for row in rows:
            dist = sum([abs(row[i] - row[i - 1]) for i in range(2, len(row))])
            if dist < mindistance[row[0]]: mindistance[row[0]] = dist
        return self.normalizescores(mindistance, smallIsBetter=1)

    def pagerankscore(self, rows):
        pageranks = dict(
            [(row[0], self.con.execute("SELECT score FROM pagerank WHERE urlid=%d" % row[0]).fetchone()[0]) for row in
             rows])
        maxrank = max(pageranks.values())
        normalizedscores = dict([(u, float(l) / maxrank) for (u, l) in pageranks.items()])
        return normalizedscores
