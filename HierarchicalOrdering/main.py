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
'''
