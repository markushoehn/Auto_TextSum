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
	now = datetime.datetime.now()
	run_pipeline(PIPELINE_SOURCE_PATH, PIPELINE_OUTPUT_PATH)
	after = datetime.datetime.now()
	print("Total time elapsed: ", (after-now))

def run_pipeline(readpath, writepath):
	dof = dict([(ix, p) for ix, p in enumerate(glob.glob(readpath))])
	shuffle(dof)
	now = datetime.datetime.now()
	print("Starting to write files, ", now)
	for k in dof:
		print("Document: ", dof[k], " (", (k+1), "/", (len(dof)), ")")

		nuggets = reader.read(dof[k])
		filepath = writepath + "topic_" + dof[k][-8:-4] + ".xml"

		table = Blackbox()
		table.add(nuggets)
		tree = []
		temp = Bubble()
		temp.nuggets.append(nuggets[0])
		tree.append(temp)

		for i, sentence in enumerate(nuggets[1:]):
			print("Sentence: ", (i+1), " / ", len(nuggets), end="\r")
			index = table.which(sentence, tree)
			if(index >= 0):
				tree[index].insert(sentence, table)
			else:
				temp = Bubble()
				temp.nuggets.append(sentence)
				tree.append(temp)

		Bubble.write(tree, filepath)
		after = datetime.datetime.now()
		print("done, elapsed: ", (after-now))
		now = datetime.datetime.now()

if __name__ == "__main__":
    main()