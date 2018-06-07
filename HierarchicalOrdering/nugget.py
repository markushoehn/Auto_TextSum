import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import *

sw = set(stopwords.words('english').extend(".,;:-_#'~/!/&()?'"))
stemmer = PorterStemmer()

class Nugget:
	def __init__(self, tuple):
		self.ix = int(tuple[0])
		self.sentence = tuple[1]
		self.pre = tuple[2]
		self.post = tuple[3]

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
		return [w for w in self.GetWords() if w.lower() not in sw]

	def GetStemmedWordsWithoutStopwords(self):
		return [stemmer.stem(w) for w in GetWordsWithoutStopwords(self)]