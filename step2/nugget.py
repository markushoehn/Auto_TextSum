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

	def GetPreSentece(self):
		return self.pre

	def GetPostSentence(self):
		return self.post
