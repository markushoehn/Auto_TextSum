## hmmmm, chicken mc nuggets

import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import *

sw = stopwords.words('english')
sw.extend(".,;:-_#'~/!/&()?'")
stemmer = PorterStemmer()

class Nugget:
	def __init__(self, tuple):
		self.ix = tuple[0]
		self.sentence = tuple[1]

		# nuggets sometimes don't have post and pre sentences?
		if(len(tuple) > 2):
			self.pre = tuple[2]
		else:
			self.pre = ""

		if(len(tuple) >= 4):
			self.post = tuple[3]
		else:
			self.post = ""

		self.stopwords = [w.lower() for w in self.GetWords() if w.lower() not in sw and len(w) > 2]

	def GetIX(self):
		return self.ix

	def GetSentence(self):
		return self.sentence

	def GetPreContext(self):
		return self.pre

	def GetPostContext(self):
		return self.post

	def GetWords(self):
		return nltk.word_tokenize(self.GetSentence())

	def GetWordsWithoutStopwords(self):
		return self.stopwords

	def GetStemmedWordsWithoutStopwords(self):
		return [stemmer.stem(w) for w in GetWordsWithoutStopwords(self)]