import nltk
from nltk.corpus import stopwords

sw = set(stopwords.words('english'))

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
		return [w for w in self.GetWords() if w.lower() not in sw and w not in ".,;:-_#'~/!/&()?'"]