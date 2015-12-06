import gp

exampletree = gp.exampletree()
# exampletree.display()
random1 = gp.makerandomtree(2)
# print random1.evaluate([7, 1])
# print random1.evaluate([2, 4])
random2 = gp.makerandomtree(2)
# print random2.evaluate([5, 3])
# print random2.evaluate([5, 20])
hiddenset = gp.buildhiddenest()
# print gp.scorefunction(random2, hiddenset)
# print gp.scorefunction(random1, hiddenset)
# random2.display()
muttree = gp.mutate(random2, 2)
# muttree.display()
# print gp.scorefunction(random2, hiddenset)
# print gp.scorefunction(muttree, hiddenset)
cross = gp.crossover(random1, random2)
cross.display()