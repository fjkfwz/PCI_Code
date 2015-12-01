import clusters

blognames, words, data = clusters.readfile('blogdata.txt')
# clust = clusters.hcluster(data, distance=clusters.tanimoto)
coords = clusters.scaledown(data)
# print coords
clusters.draw2d(coords, blognames, jpeg='blogs2d.jpg')
