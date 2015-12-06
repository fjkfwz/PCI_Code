from random import random, randint, choice
from copy import deepcopy
from math import log


class fwrapper:
    def __init__(self, function, childcount, name):
        self.function = function
        self.childcount = childcount
        self.name = name


class node:
    def __init__(self, fw, children):
        self.function = fw.function
        self.name = fw.name
        self.children = children

    def evaluate(self, inp):
        results = [n.evaluate(inp) for n in self.children]
        return self.function(results)

    def display(self, indent=0):
        print (' ' * indent) + self.name
        for c in self.children:
            c.display(indent + 1)


class paramnode:
    def __init__(self, idx):
        self.idx = idx

    def evaluate(self, inp):
        return inp[self.idx]

    def display(self, indent=0):
        print '%sp%d' % (' ' * indent, self.idx)


class constnode:
    def __init__(self, v):
        self.v = v

    def evaluate(self, inp):
        return self.v

    def display(self, indent=0):
        print '%s%d' % (' ' * indent, self.v)


addw = fwrapper(lambda l: l[0] + l[1], 2, 'add')
subw = fwrapper(lambda l: l[0] - l[1], 2, 'subtract')
mulw = fwrapper(lambda l: l[0] * l[1], 2, 'multiply')


def iffunc(l):
    if l[0] > 0:
        return l[1]
    else:
        return l[2]


ifw = fwrapper(iffunc, 3, 'if')


def isgreater(l):
    if l[0] > l[1]:
        return 1
    else:
        return 0


gtw = fwrapper(isgreater, 2, 'isgreater')
flist = [addw, mulw, ifw, gtw, subw]


def exampletree():
    return node(ifw, [
        node(gtw, [paramnode(0), constnode(3)]),
        node(addw, [paramnode(1), constnode(5)]),
        node(subw, [paramnode(1), constnode(2)])
    ])


def makerandomtree(pc, maxdepth=4, fpr=0.5, ppr=0.6):
    if random() < fpr and maxdepth > 0:
        f = choice(flist)
        children = [makerandomtree(pc, maxdepth - 1, fpr, ppr)
                    for i in range(f.childcount)]
        return node(f, children)
    elif random() < ppr:
        return paramnode(randint(0, pc - 1))
    else:
        return constnode(randint(0, 10))


def hiddenfunction(x, y):
    return x ** 2 + 2 * y + 3 * x + 5


def buildhiddenest():
    rows = []
    for i in range(200):
        x = randint(0, 40)
        y = randint(0, 40)
        rows.append([x, y, hiddenfunction(x, y)])
    return rows


def scorefunction(tree, s):
    dif = 0
    for data in s:
        v = tree.evaluate([data[0], data[1]])
        dif += abs(v - data[2])
    return dif


def crossover(t1, t2, probswap=0.7, top=1):
    if random() < probswap and not top:
        return deepcopy(t2)
    else:
        result = deepcopy(t1)
        if isinstance(t1, node) and isinstance(t2, node):
            result.children = [crossover(c, choice(t2.children), probswap, 0) for c in t1.children]
        return result


def mutate(t, pc, probchange=0.1):
    if random() < probchange:
        return makerandomtree(pc)
    else:
        result = deepcopy(t)
        if isinstance(t, node):
            result.children = [mutate(c, pc, probchange) for c in t.children]
        return result


def evolve(pc, popsize, rankfunction, maxgen=500, mutationrate=0.1, breedinggrate=0.4, pexp=0.7, pnew=0.05):
    def selectindex():
        return int(log(random()) / log(pexp))

    population = [makerandomtree(pc) for i in range(popsize)]
    for i in range(maxgen):
        scores = rankfunction(population)
        print scores[0][0]
        if scores[0][0] == 0: break
        newpop = [scores[0][1], scores[1][1]]
        while len(newpop) < popsize:
            if random() > pnew:
                newpop.append(mutate(
                    crossover(scores[selectindex()][1],
                              scores[selectindex()][1],
                              probswap=breedinggrate),
                    pc, probchange=mutationrate))
        else:
            newpop.append(makerandomtree(pc))
        population = newpop
    scores[0][1].display()
    return scores[0][1]


def getrankfunction(dataset):
    def rankfunction(population):
        scores = [(scorefunction(t, dataset), t) for t in population]
        scores.sort()
        return scores

    return rankfunction


def gridgame(p):
    max = (3, 3)
    lastmove = [-1, -1]
    location = [[randint(0, max[0]), randint(0, max[1])]]
    location.append([(location[0][0] + 2) % 4, (location[0][1] + 2) % 4])
    for o in range(50):
        for i in range(2):
            locs = location[i][:] + location[1 - i][:]
            locs.append(lastmove[i])
            move = p[i].evaluate(locs) % 4
            if lastmove[i] == move: return 1 - i
            lastmove[i] = move
            if move == 0:
                location[i][0] -= 1
                if location[i][0] < 0: location[i][0] = 0
            if move == 1:
                location[i][0] += 1
                if location[i][0] > max[0]: location[i][0] = max[0]
            if move == 2:
                location[i][1] -= 1
                if location[i][1] < 0: location[i][1] = 0
            if move == 3:
                location[i][1] += 1
                if location[i][1] > max[1]: location[i][1] = max[1]
            if location[i] == location[1 - i]: return i
    return -1


def tournament(p1):
    losses = [0 for p in p1]
    for i in range(len(p1)):
        for j in range(len(p1)):
            if i == j: continue
            winner = gridgame([p1[i], p1[j]])
            if winner == 0:
                losses[j] += 2
            elif winner == 1:
                losses[i] += 2
            elif winner == -1:
                losses[i] += 1
                losses[i] += 1
                pass
        z = zip(losses, p1)
        z.sort()
        return z


class humanplayer:
    def evaluate(self, board):
        me = tuple(board[0:2])
        others = [tuple(board[x:x + 2]) for x in range(2, len(board) - 1, 2)]
        for i in range(4):
            for j in range(4):
                if (i, j) == me:
                    print 'O',
                elif (i, j) in others:
                    print 'X',
                else:
                    print '.',
            print
        print "YOU LAST MOVE WAS %d" % board[len(board) - 1]
        print ' 0'
        print '2 3'
        print ' 1'
        print 'Enter move: ',
        move = int(raw_input())
        return move
