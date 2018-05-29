from nugget import Nugget
from BubbleTree import Tree 
import reader
import glob, nltk

dof = dict([(ix, p) for ix, p in enumerate(glob.glob("../Corpus/Trees/Input/*.txt"))])
for k in dof:
	print(k, dof[k])

while True:
	try:
		file_no = int(input('Enter the number of the desired file: '))
		
		if file_no in dof:
			nuggets = reader.read(dof[file_no])
			break
		else:
			print('file not available!')
	except (ValueError, NameError, TypeError):
		print('Oops! Wrong input!')

print(nuggets[0].GetWords());
print(nuggets[0].GetWordsWithoutStopwords());


# word 2 vec
# https://datascience.stackexchange.com/questions/23969/sentence-similarity-prediction
'''
tmp =  [nltk.word_tokenize(n.GetSentence()) for n in nuggets]
print(type(tmp))
print(len(tmp))

li = []
for i in tmp:
	for j in i:
		li.append(j.lower())
print(len(li))

fdist = nltk.FreqDist(li)
print(fdist.most_common(50))

print([n.GetIX() for n in nuggets])

tree = Tree.createListTree(nuggets)
Tree.write([tree])


## similarity between two sentences with nltk:

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

both(stops(nltk.word_tokenize(a)), stops(nltk.word_tokenize(b)))

from functools import reduce
reduce((lambda x, y: x + y), [a for b in result for a in b if a]) / len([a for b in result for a in b])


'''
