import math
from nltk.corpus import wordnet as wn
from random import randint
from functools import reduce

# TODO: make constant .py file for strings
SENTENCE_SIMILAR = "similar"
SENTENCE_GENERAL = "general"
SENTENCE_SPECIFIC = "speficic"
THRESHOLD = 0.09

class Blackbox(object):
	""" blackbox where the magic happens """
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

	def tf(self, word, sentence):
		return sentence.count(word) / len(sentence)

	def n_contain(self, word, table):
		return sum(1 for blob in table if word in blob)

	def idf(self, word, table):
		return math.log(len(table) / (1 + self.n_contain(word, table)))

	def tfidf(self, sentence, table):
		value = 0
		for word in sentence:
			value += self.tf(word, sentence) * self.idf(word, table)
		return value / len(sentence)

	# compares two sentences
	# returns similar, if they are similar in meaning
	# return genereal when the first is more summarizing
	# return specific when the second is mor summarizing
	def compare(self, sentence, nuggets):
		wordListFirst = sentence.GetWordsWithoutStopwords()
		wordListSecond = [item for sublist in nuggets for item in sublist.GetWordsWithoutStopwords()]

		result = self.nltk_path_similarity(wordListFirst, wordListSecond)

		if(result >= THRESHOLD ):
			return SENTENCE_SIMILAR
		
		resultFirst = self.tfidf(wordListFirst, self.table)
		resultSecond = self.tfidf(wordListSecond, self.table)

		if(resultFirst >= resultSecond):
			return SENTENCE_SPECIFIC
		else:
			return SENTENCE_GENERAL

	def get_all_words(self, bubble):
		# TODO: go over all sub bubbles
		listofwords = []
		for x in bubble.nuggets:
			listofwords.extend(x.GetWordsWithoutStopwords())
		#if(bubble.bubbles):
		#	for x in bubble.bubbles:
		#		listofwords.extend(self.get_all_words(x))
		return listofwords


	# compares a list of Bubbles against an item
	# return which is the best fit for the item
	# returning -1 means that none fit
	def which(self, sentence, bubbles):
		wordListFirst = sentence.GetWordsWithoutStopwords()
		
		# calculate values for sentence and bubbles
		bubbleValues = []
		for x in bubbles:
			wordListSecond = self.get_all_words(x)
			bubbleValues.append(self.tfidf(wordListSecond, self.table))

		sentenceValue = self.tfidf(wordListFirst, self.table)

		# find the hightest value
		valueIndex = -1
		value = -1
		for (index,x) in enumerate(bubbleValues):
			if(value < x):
				valueIndex = index
				value = x

		# return either
		if(value > sentenceValue):
			return valueIndex


		return -1
