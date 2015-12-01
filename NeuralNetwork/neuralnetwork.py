from math import tanh
from sqlite3 import dbapi2 as sqlite


class searchnet:
    def __init__(self, dbname):
        self.con = sqlite.connect(dbname)

    def __del__(self):
        self.con.close()

    def maketables(self):
        self.con.execute('CREATE TABLE hiddenode(create_key)')
        self.con.execute('CREATE TABLE wordhidden(fromid,toid,strength)')
        self.con.execute('CREATE TABLE hiddenurl(fromid,toid,strength)')
        self.con.commit()

    def getstrength(self, fromid, toid, layer):
        if layer == 0:
            table = 'wordhidden'
        else:
            table = 'hiddenurl'
        res = self.con.execute(
            'SELECT strength FROM %s WHERE fromid = %s AND toid = %s' % (table, fromid, toid)).fetchone()
        if res == None:
            if layer == 0: return -0.2
            if layer == 1: return 0
        return res[0]

    def setstrength(self, fromid, toid, layer, strength):
        if layer == 0:
            table = "wordhidden"
        else:
            table = "hiddenurl"
        res = self.con.execute(
            "SELECT strength FROM %s WHERE fromid = %d AND toid = %d" % (table, fromid, toid)).fetchone()
        if res == None:
            self.con.execute(
                "INSERT INTO %s (fromid, toid, strength) VALUES (%d,%d,%f)" % (table, fromid, toid, strength))
        else:
            rowid = res[0]
            self.con.execute("UPDATE %s SET strength = %f WHERE rowid = %d" % (table, strength, rowid))

    def generatehiddennode(self, wordids, urls):
        if len(wordids) > 3: return None
        createkey = "_".join(sorted([str(wi) for wi in wordids]))
        res = self.con.execute("SELECT rowid FROM hiddenode WHERE create_key = '%s'" % createkey).fetchone()

        if res == None:
            cur = self.con.execute("INSERT INTO hiddenode (create_key) VALUES ('%s')" % createkey)
            hiddenid = cur.lastrowid
            for wordid in wordids:
                self.setstrength(wordid,hiddenid,0, 1.0/len(wordids))
            for urlid in urls:
                self.setstrength(hiddenid, urlid, 1, 0.1)
            self.con.commit()

