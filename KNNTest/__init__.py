import socks
import socket
import newsfeatures
import docclass
import clusters
import nnmf
from numpy import *

socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 1080)
socket.socket = socks.socksocket
allw, artw, artt = newsfeatures.getarticlewords()
wordmatrix, wordvec = newsfeatures.makematrix(allw, artw)
v = matrix(wordmatrix)
weights, feat = nnmf.factorize(v, pc=20, iter=50)