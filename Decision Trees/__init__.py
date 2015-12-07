import treepredict
import zillow

# print treepredict.my_data
# print treepredict.giniimpurity(treepredict.my_data)
# print treepredict.entropy(treepredict.my_data)
# set1, set2 = treepredict.divideset(treepredict.my_data, 2, 'yes')
# print treepredict.entropy(set1)
# print treepredict.giniimpurity(set1)
# tree = treepredict.buildtree(treepredict.my_data)
# treepredict.printtree(tree)
# print "----------------------"
# treepredict.drawtree(tree,jpeg='treeview.jpg')
# treepredict.prune(tree, 0.1)
# treepredict.printtree(tree)
# print "----------------------"
# treepredict.prune(tree,1.0)
# treepredict.printtree(tree)
# print treepredict.mdclassify(['google', 'None', 'yes', None], tree)
# print treepredict.mdclassify(['google', 'France', None, None], tree)
housedata = zillow.getpricelist()
print housedata
housetree = treepredict.buildtree(housedata, scoref=treepredict.variance)
treepredict.drawtree(housedata, 'housetree.jpg')
