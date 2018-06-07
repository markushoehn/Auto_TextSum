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

def nltk_path_similarity(lista,listb):
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

	result = both(lista, listb)

	value = reduce((lambda x, y: x + y), [a for b in result for a in b if a]) / len([a for b in result for a in b])
	return value
	

def same_words(lista,listb):
	count = 0
	for x in lista:
		for y in listb:
			if(x.lower() == y.lower()):
				count = count + 1
	return count

# compares two sentences
# returns similar, if they are similar in meaning
# return genereal when the first is more summarizing
# return specific when the second is mor summarizing
def compare(sentence, nuggets):
	wordListFirst = sentence.GetWordsWithoutStopwords()
	wordListSecond = nuggets[0].GetWordsWithoutStopwords()

	result = nltk_path_similarity(wordListFirst, wordListSecond)

	if(result >= 0.100 ):
		return SENTENCE_SIMILAR
	if(result >= 0.08 ):
		return SENTENCE_GENERAL

	return SENTENCE_SPECIFIC


# compares a list of Bubbles against an item
# return which is the best fit for the item
# returning -1 means that none fit
def which(sentence, bubbles):
	wordListFirst = sentence.GetWordsWithoutStopwords()
	result = []
	for x in bubbles:
		wordListSecond = x.nuggets[0].GetWordsWithoutStopwords()
		result.append(same_words(wordListFirst,wordListSecond))

	valueIndex = -1
	value = 0
	for (index,x) in enumerate(result):
		if(x > 1):
			if(value < x):
				valueIndex = index
				value = x
	
	print(value, valueIndex)
	return valueIndex