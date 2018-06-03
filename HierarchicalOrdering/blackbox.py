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

from nltk.corpus import wordnet as ws
from random import randint

def compare(first, second):
	test = randint(0,3)
	# TODO: make constants for strings
	# TODO: implement this function
	if(test == 0):
		return "specific"
	if(test==1):
		return "general"
	if(test==2):
		return "newtopic"