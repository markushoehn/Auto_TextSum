import math
from nltk.corpus import wordnet as wn
from random import randint
from functools import reduce

# TODO: make constant .py file for strings
SENTENCE_SIMILAR = "similar"
SENTENCE_GENERAL = "general"
SENTENCE_SPECIFIC = "speficic"
THRESHOLD = 0.25

class Blackbox(object):
	""" blackbox where the magic happens """
	def __init__(self):
		super(Blackbox, self).__init__()
		self.table = []
		self.enableGeneralSentences = False
		# self.synsets = dict([(w,wn.synsets(w)[0]) for w in self.stopwords])

	def setGeneralSentences(val):
		self.enableGeneralSentences = val


	def add(self, sentencelist):
		self.table = [item for sublist in sentencelist for item in sublist.GetWordsWithoutStopwords()]

	def nltk_path_similarity(self, lista, listb):
		def sim(x,y):
			try:
				a = wn.synsets(y)[0]
				b = wn.synsets(x)[0]
				res = a.path_similarity(b)
			except Exception as e:
				return 0
			if(res):
				return res
			return 0

		result = [[sim(x,y) for y in listb] for x in lista]
		flatten = [max(b) for b in result]

		#flatten = [a for b in result for a in b]
		#flatten = [a for a in flatten if a and a != 0]
		value = reduce((lambda x, y: x + y), flatten) / len(flatten)
		#value = median(flatten)
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

	def compare(self, sentence, nuggets):
		"""
		compares two sentences
		returns similar, if they are similar in meaning
		return genereal when the first is more summarizing
		return specific when the second is mor summarizing
		"""
		
		sentenceList = sentence.GetWordsWithoutStopwords()
		nuggetsList2 = [self.tfidf(sublist.GetWordsWithoutStopwords(), self.table) for sublist in nuggets]

		if(self.enableGeneralSentences):
			result = self.nltk_path_similarity(sentenceList, nuggetsList)
			if(result >= THRESHOLD):
				return SENTENCE_SIMILAR
		
		sentenceResult = self.tfidf(sentenceList, self.table)
		nuggetsResult = reduce((lambda x,y: x+y), nuggetsList2) / len(nuggetsList2)

		if(sentenceResult >= nuggetsResult):
			return SENTENCE_SIMILAR
		else:
			return SENTENCE_SPECIFIC

	def get_all_words(self, bubble):
		"""
		return all words in a bubble
		"""
		listofwords = []
		for x in bubble.nuggets:
			listofwords.extend(x.GetWordsWithoutStopwords())
		#if(bubble.bubbles):
		#	for x in bubble.bubbles:
		#		listofwords.extend(self.get_all_words(x))
		return listofwords

	def which(self, sentence, bubbles):
		"""
		compares a list of Bubbles against an item
		return which is the best fit for the item
		returning -1 means that none fit
		"""
		wordListFirst = sentence.GetWordsWithoutStopwords()
		
		# calculate values for sentence and bubbles
		bubbleValues = []
		for x in bubbles:
			wordListSecond = self.get_all_words(x)
			bubbleValues.append(self.nltk_path_similarity(wordListFirst, wordListSecond))

		# find the hightest value
		valueIndex = -1
		value = -1
		for (index,x) in enumerate(bubbleValues):
			if(value < x):
				valueIndex = index
				value = x

		# return either
		if(value > THRESHOLD):
			return valueIndex


		return -1
