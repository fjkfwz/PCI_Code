import socks
import socket
import newsfeature
import docclass
import clusters
import nmf
from numpy import *

socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 1080)
socket.socket = socks.socksocket

allw, artw, artt = newsfeature.getarticlewords()
wordmatrix, wordvec = newsfeature.makematrix(allw, artw)
# print wordvec[0:10]
# print "------------"
# print artt[1]
# print "------------"
# print wordmatrix[1][0:10]
#
#
# def wordmatrixfeatures(x):
#     return [wordvec[w] for w in range(len(x)) if x[w] > 0]
#
#
# print wordmatrixfeatures(wordmatrix[0])
# print "-------------"
#
# classifier = docclass.naivebayes(wordmatrixfeatures)
# classifier.setdb('newstest.db')
# print artt[0]
# print "--------------"
# classifier.train(wordmatrix[0], 'iraq')
# print artt[0]
# print "--------------"
# classifier.train(wordmatrix[1], 'india')
# print artt[0]
# print "--------------"
# print classifier.classify(wordmatrix[1])
#
# clust = clusters.hcluster(wordmatrix)
# clusters.drawdendrogram(clust, artt, jpeg='new.jpg')

# l1 = [[1, 2, 3], [4, 5, 6]]
# print l1
# m1 = matrix(l1)
# print m1
# m2 = matrix([[1, 2], [3, 4], [5, 6]])
# print m2
# print m1 * m2
# w, h = nmf.factorize(m1 * m2, pc=3, iter=100)
# print w, h
# print w * h
# print m1 * m2

v = matrix(wordmatrix)
weights, feat = nmf.factorize(v, pc=20, iter=50)
topp, pn = newsfeature.showfeatures(weights, feat, artt, wordvec)
newsfeature.showarticles(artt, topp, pn)
