# A dictionary of movie critics and their ratings of a small
# set of movies
critics = {'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
                         'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5,
                         'The Night Listener': 3.0},
           'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
                            'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0,
                            'You, Me and Dupree': 3.5},
           'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
                                'Superman Returns': 3.5, 'The Night Listener': 4.0},
           'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
                            'The Night Listener': 4.5, 'Superman Returns': 4.0,
                            'You, Me and Dupree': 2.5},
           'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
                            'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
                            'You, Me and Dupree': 2.0},
           'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
                             'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
           'Toby': {'Snakes on a Plane': 4.5, 'You, Me and Dupree': 1.0, 'Superman Returns': 4.0}}

from math import sqrt


def sim_distance(prefs, person1, person2):
    si = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1
    if len(si) == 0: return 0
    sum_of_squrares = sum(
        [pow(prefs[person1][item] - prefs[person2][item], 2) for item in prefs[person1] if item in prefs[person2]])
    return 1 / (1 + sqrt(sum_of_squrares))


def sim_pearson(prefs, preson1, preson2):
    si = {}
    for item in prefs[preson1]:
        if item in prefs[preson2]: si[item] = 1
    n = len(si)
    if n == 0: return 1
    sum1 = sum([prefs[preson1][it] for it in si])
    sum2 = sum([prefs[preson2][it] for it in si])
    sum1Sq = sum([pow(prefs[preson1][it], 2) for it in si])
    sum2Sq = sum([pow(prefs[preson2][it], 2) for it in si])
    pSum = sum([prefs[preson1][it] * prefs[preson2][it] for it in si])
    num = pSum - (sum1 * sum2 / n)
    den = sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n))
    if den == 0: return 0
    r = num / den
    return r


def topMatches(prefs, person, n=5, similarity=sim_pearson):
    scores = [(similarity(prefs, person, other), other) for other in prefs if other != person]
    scores.sort()
    scores.reverse()
    return scores[0:n]


def getRecommendations(prefs, person, similarity=sim_pearson):
    totals = {}
    simSum = {}
    for other in prefs:
        if other == person: continue
        sim = similarity(prefs, person, other)
        if sim <= 0: continue
        for item in prefs[other]:
            if item not in prefs[person] or prefs[person][item] == 0:
                totals.setdefault(item, 0)
                totals[item] += prefs[other][item] * sim
                simSum.setdefault(item, 0)
                simSum[item] += sim
    rankings = [(total / simSum[item], item) for item, total in totals.items()]
    rankings.sort()
    rankings.reverse()
    return rankings


def getRecommendedItem(prefs, itemMatch, user):
    userRatings = prefs[user]
    scores = {}
    totalSim = {}
    for (item, rating) in userRatings.items():
        for (similarity, item2) in itemMatch[item]:
            if item2 in userRatings: continue
            scores.setdefault(item2, 0)
            scores[item2] += similarity * rating
            totalSim.setdefault(item2, 0)
            totalSim[item2] += similarity
    ranking = [(score / totalSim[item], item) for item, score in scores.items()]
    ranking.sort()
    ranking.reverse()
    return ranking


def transfromPrefs(prefs):
    result = {}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item, {})
            result[item][person] = prefs[person][item]
    return result


def calculateSimilarItem(prefs, n=10):
    result = {}
    itemPrefs = transfromPrefs(prefs)
    c = 0
    for item in itemPrefs:
        c += 1
        if c % 100 == 0: print "%d / %d" % (c, len(itemPrefs))
        scores = topMatches(itemPrefs, item, n=n, similarity=sim_distance)
        result[item] = scores
    return result


def loadMovieLens(path='data'):
    movies = {}
    for line in open(path + '/u.item'):
        (id, title) = line.split("|")[0:2]
        movies[id] = title
    prefs = {}
    for line in open(path + '/u.data'):
        (user, movieid, rating, ts) = line.split('\t')
        prefs.setdefault(user, {})
        prefs[user][movies[movieid]] = float(rating)
    return prefs
