from nugget import Nugget
import csv

def read(path):
	with open(path, 'r') as csvfile:
		file = csv.reader(csvfile, delimiter='\t')
		res = [Nugget(t) for t in file]
		return res