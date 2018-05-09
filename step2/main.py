from nugget import Nugget
import reader
import glob

dof = dict([(ix, p) for ix, p in enumerate(glob.glob("../Corpus/Trees/Input/*.txt"))])
for k in dof:
	print(k, dof[k])

while True:
	try:
		file_no = int(input('Enter the number of the desired file: '))
		
		if file_no in dof:
			nuggets = reader.read(dof[int(file_no)])
			break
		else:
			print('file not available!')
	except (ValueError, NameError, TypeError):
		print('Oops! Wrong input!')

print([n.GetIX() for n in nuggets])