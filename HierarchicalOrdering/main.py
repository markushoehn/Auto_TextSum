from nugget import Nugget
import reader
import glob
from BubbleTree import Tree 

filepath = "../Corpus/Trees/Input/"
dof = dict([(ix, p) for ix, p in enumerate(glob.glob(filepath + "*.txt"))])
print(dof)

while True:
	try:
		file_no = int(input('Enter the number of the desired file: '))
		
		if file_no in dof:
			nuggets = reader.read(dof[int(file_no)])
			break
		else:
			print('file not available!')
	except (ValueError):
		print('Oops! Wrong input!')

print([n.GetIX() for n in nuggets])

tree = Tree.createListTree(nuggets)
Tree.write([tree])