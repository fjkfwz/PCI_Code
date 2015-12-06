import gp

# exampletree = gp.exampletree()
# exampletree.display()
# random1 = gp.makerandomtree(2)
# random1.display()
# print random1.evaluate([7, 1])
# print random1.evaluate([2, 4])
# random2 = gp.makerandomtree(2)
# print random2.evaluate([5, 3])
# print random2.evaluate([5, 20])
# hiddenset = gp.buildhiddenest()
# print hiddenset
# print gp.scorefunction(random2, hiddenset)
# print gp.scorefunction(random1, hiddenset)
# random2.display()
# print "---------------------------"
# muttree = gp.mutate(random2, 2)
# muttree.display()
# print gp.scorefunction(random2, hiddenset)
# print gp.scorefunction(muttree, hiddenset)
# cross = gp.crossover(random1, random2)
# cross.display()
# rf = gp.getrankfunction(gp.buildhiddenest())
# gp.evolve(2, 500, rf, mutationrate=0.2, breedinggrate=0.1, pexp=0.7, pnew=0.1)
# ----------------------------------------------------------
# p1 = gp.makerandomtree(5)
# p2 = gp.makerandomtree(5)
# print gp.gridgame([p1, p2])
winner = gp.evolve(5, 100, gp.tournament, maxgen=50)
# print winner
print gp.gridgame([winner, gp.humanplayer()])
