import recommendation

# print recommendation.sim_distance(recommendation.critics, 'Lisa Rose', 'Gene Seymour')
# print recommendation.sim_pearson(recommendation.critics, 'Lisa Rose', 'Gene Seymour')
# print recommendation.topMatches(recommendation.critics, 'Toby', n=3)

# print recommendation.getRecommendations(recommendation.critics,'Toby')
# print recommendation.getRecommendations(recommendation.critics,'Toby', similarity=recommendation.sim_distance)

# movies = recommendation.transfromPrefs(recommendation.critics)
# print recommendation.getRecommendations(movies,'Just My Luck')
# print recommendation.topMatches(movies,'Superman Returns')

# print recommendation.calculateSimilarItem(recommendation.critics)

prefs = recommendation.loadMovieLens()
print recommendation.getRecommendations(prefs, '87')[0:30]
itemsim = recommendation.calculateSimilarItem(prefs,n=50)
print recommendation.getRecommendedItem(prefs, itemsim, '87')[0:30]

# print recommendation.getRecommendedItem(recommendation.critics,itemsim,'Toby')