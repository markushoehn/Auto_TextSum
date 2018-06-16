import math
from nltk.corpus import wordnet as wn
from random import randint
from functools import reduce

# TODO: make constant .py file for strings
SENTENCE_SIMILAR = "similar"
SENTENCE_GENERAL = "general"
SENTENCE_SPECIFIC = "speficic"

class Blackbox(object):
	""" tree class for bubbles and nuggets and trash """
	def __init__(self):
		super(Blackbox, self).__init__()
		self.table = []
		self.dict = {}

	def add(self, sentencelist):
		self.table = [item for sublist in sentencelist for item in sublist.GetWordsWithoutStopwords()]

	def nltk_path_similarity(self, lista,listb):
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
		

	def same_words(self, lista,listb):
		count = 0
		for x in lista:
			for y in listb:
				if(x.lower() == y.lower()):
					count = count + 1

		return count

	def tf(self, word, sentence):
		return sentence.count(word) / len(sentence)

	def n_contain(self, word):
		return sum(1 for blob in self.table if word in blob)

	def idf(self, word):
		return math.log(len(self.table) / (1 + self.n_contain(word)))

	def tfidf(self, sentence):
		value = 0
		for word in sentence:
			value += self.tf(word, sentence) * self.idf(word)
		return value / len(sentence)

	# compares two sentences
	# returns similar, if they are similar in meaning
	# return genereal when the first is more summarizing
	# return specific when the second is mor summarizing
	def compare(self, sentence, nuggets):
		wordListFirst = sentence.GetWordsWithoutStopwords()
		wordListSecond = [item for sublist in nuggets for item in sublist.GetWordsWithoutStopwords()]

		result = self.nltk_path_similarity(wordListFirst, wordListSecond)

		if(result >= 0.09 ):
			return SENTENCE_SIMILAR
		
		resultFirst = self.tfidf(wordListFirst)
		resultSecond = self.tfidf(wordListSecond)

		if(resultFirst >= resultSecond):
			return SENTENCE_SPECIFIC
		else:
			return SENTENCE_GENERAL


	# compares a list of Bubbles against an item
	# return which is the best fit for the item
	# returning -1 means that none fit
	def which(self, sentence, bubbles):
		wordListFirst = sentence.GetWordsWithoutStopwords()
		result = []
		for x in bubbles:
			wordListSecond = [item for sublist in x.nuggets for item in sublist.GetWordsWithoutStopwords()]
			result.append(self.same_words(wordListFirst,wordListSecond))

		valueIndex = -1
		value = 0
		for (index,x) in enumerate(result):
			if(x > 2):
				if(value < x):
					valueIndex = index
					value = x
		
		return valueIndex
