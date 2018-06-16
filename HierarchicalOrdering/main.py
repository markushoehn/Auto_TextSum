from nugget import Nugget
from bubble import Bubble
from random import shuffle
from blackbox import Blackbox
import reader
import glob, nltk
import datetime

NUGGETS_SOURCE_PATH = "../Corpus/Trees/Input/*.txt"
PIPELINE_SOURCE_PATH = "../Pipeline/01_selected_nuggets/*.txt"
PIPELINE_OUTPUT_PATH = "../Pipeline/02_hierarchical_trees/"

def main():
	dof = dict([(ix, p) for ix, p in enumerate(glob.glob(NUGGETS_SOURCE_PATH))])
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

	shuffled = [i for i in nuggets[0:50]]
	shuffle(shuffled)

	tree = Bubble()
	for x in shuffled:
		tree.insert(x)
	Bubble.write([tree])
	tree.draw()

def run_pipeline():
	dof = dict([(ix, p) for ix, p in enumerate(glob.glob(PIPELINE_SOURCE_PATH))])
	shuffle(dof)
	now = datetime.datetime.now()
	print("Starting to write files, ", now)
	for k in dof:
		print("Document: ", dof[k], " (", (k+1), "/", (len(dof)), ")")

		nuggets = reader.read(dof[k])
		filepath = PIPELINE_OUTPUT_PATH + "topic_" + dof[k][-8:-4] + ".xml"

		table = Blackbox()
		table.add(nuggets)
		tree = Bubble()

		for i, sentence in enumerate(nuggets):
			print("Sentence: ", (i+1), " / ", len(nuggets), end="\r")
			tree.insert(sentence, table)
		Bubble.write([tree], filepath)
	after = datetime.datetime.now()
	print("done, elapsed: ", (after-now))

if __name__ == "__main__":
    run_pipeline()

'''
# word 2 vec
# https://datascience.stackexchange.com/questions/23969/sentence-similarity-prediction

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



## similarity between two sentences with nltk:



'''
