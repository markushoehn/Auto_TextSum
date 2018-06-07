# input csv
# id, precontext, sentence, postcontext

# out
# tree of bubbles and nuggets

# 1 Baseline
#   Create Random Tree
#   Create Straight Tree
# 2 NaiveBayesClassifier
#   learning against GoldStandart
#   features: sentences, context, etc
# 3 freqDist
#   häufige Vorkommende Wörter in Sätzen
#   stopword, lematization
#   häufige Wörter besser bewerten
# 4 WordNet Similarity
#   get similarity of all words of one sentence against another
#   find most similiar sentences, the most similar sentence is the one at the top
# 5 LDA
#   find topics for different Trees
# 6 Word Embedings
#   Vectoren of words, sentences, sort them and create tree
# 7 WordNet Synonyms
#   find most common synonyms in sentences, create tree with most common on top

from nltk.corpus import wordnet as wn
from random import randint
from functools import reduce

# TODO: make constant .py file for strings
SENTENCE_SIMILAR = "similar"
SENTENCE_GENERAL = "general"
SENTENCE_SPECIFIC = "speficic"

# compares two sentences
# returns similar, if they are similar in meaning
# return genereal when the first is more summarizing
# return specific when the second is mor summarizing
def compare(first, second):
	test = randint(0,9)
	stopa = first.GetStemmedWordsWithoutStopwords()
	stopb = second[0].GetStemmedWordsWithoutStopwords()
	def sim(x,y):
		try:
			a = wn.synsets(y)[0]
			b = wn.synsets(x)[0]
			res = a.path_similarity(b)
		except Exception as e:
			return 0
		return res

	def both(a,b):
		return [[sim(x,y) for y in b] for x in a]

	result = both(stopa, stopb)

	value = reduce((lambda x, y: x + y), [a for b in result for a in b if a]) / len([a for b in result for a in b])

	if(value >= 0.66 ):
		return SENTENCE_GENERAL
	if(value <= 0.33):
		return SENTENCE_SPECIFIC

	return SENTENCE_SIMILAR

# compares a list of Bubbles against an item
# return which is the best fit for the item
# returning -1 means that none fit
def which(list, item):
	test = randint(-len(list),len(list)-1)
	return test