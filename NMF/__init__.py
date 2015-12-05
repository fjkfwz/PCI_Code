import socks
import socket
import newsfeature
import docclass
import clusters
import nmf
from numpy import *

out = file('matrix.txt', "w+")
socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 1080)
socket.socket = socks.socksocket

allw, artw, artt = newsfeature.getarticlewords()

wordmatrix, wordvec = newsfeature.makematrix(allw, artw)

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

# l1 = [[1, 2, 3,0], [4, 5, 6,0]]
# print l1
# m1 = matrix(l1)
# print m1
# m2 = matrix([[1, 2], [3, 4], [5, 6], [0, 0]])
# print m2
# print m1 * m2
# w, h = nmf.factorize(m2, pc=4, iter=100)
# print w, h
# print w * h
# print m1 * m2
# v = matrix(wordmatrix)
# for i in range(shape(v)[0]):
#         print >> out, v[i]
#         print v[i]
# out.close()
v=matrix(wordmatrix)
weights, feat = nmf.factorize(v, pc=10, iter=50)
topp, pn = newsfeature.showfeatures(weights, feat, artt, wordvec)
newsfeature.showarticles(artt, topp, pn)
