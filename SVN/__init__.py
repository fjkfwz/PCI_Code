import advancedclassify
import bingmapsapi
from svmutil import *
import json

# agesonly = advancedclassify.loadmatch('agesonly.csv', allnum=True)
# matchmaker = advancedclassify.loadmatch('matchmaker.csv')
# advancedclassify.plotagematches(agesonly)
# avgs = advancedclassify.lineartrain(agesonly)
# print advancedclassify.dpclassify([30, 25], avgs)
# print advancedclassify.dpclassify([25, 40], avgs)
# print advancedclassify.dpclassify([48, 20], avgs)
numbericalset = bingmapsapi.loadnumerical()
# out = open('numbericalset.txt', 'w+')
# print numbericalset
# json.dump(json.JSONEncoder(numbericalset), out)
# out.close()
scaledset, scalef = advancedclassify.scaledata(numbericalset)
# avgs = advancedclassify.lineartrain(scaledset)
# print numbericalset[0].match
# print advancedclassify.dpclassify(scalef(numbericalset[0].data), avgs)
# print numbericalset[11].match
# print advancedclassify.dpclassify(scalef(numbericalset[11].data), avgs)

answers, inputs = [r.match for r in scaledset], [r.data for r in scaledset]
prob = svm_problem(answers, inputs)
# m = svm_train(prob, '-t 3')
# svm_save_model('test.model', m)
m = svm_load_model('test.model')
# newrow = [28.0, -1, -1, 26.0, -1, 1, 2, 0.8]
# predicted_labels0 = svm_predict(scalef(newrow), m)
# print predicted_labels0
# newrow = [28.0, -1, 1, 26.0, -1, 1, 2, 0.8]
# predicted_labels1 = svm_predict(scalef(newrow), m)
# print predicted_labels1
guesses = svm_train(prob, '-v 4')
print guesses
