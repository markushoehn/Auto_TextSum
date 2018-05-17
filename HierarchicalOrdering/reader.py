from nugget import Nugget
import csv

def read(path):
	with open(path, 'r') as csvfile:
		return [Nugget(t) for t in csv.reader(csvfile, delimiter='\t')]