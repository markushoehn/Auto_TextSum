import xml.etree.ElementTree as ET
from random import randint
		
class Tree(object):
	""" tree class for bubbles and nuggets and trash """
	def __init__(self):
		super(Tree, self).__init__()
		self.nuggets = []
		self.bubbles = []
		self.trash = []

	def write(trees):
		root = ET.Element('root')

		""" TOOD: should add Nuggets and Bubbles objects individually"""
		def traverse(root, sub):
			if type(sub) is Tree:
				for n in sub.nuggets:
					ET.SubElement(root, 'Nugget', id=n)
				for bubble in sub.bubbles:
					b = ET.SubElement(root, 'Bubble', name="name")
					traverse(b, bubble)

		for bubbles in trees:
			b = ET.SubElement(root, 'Bubble', name="name")
			traverse(b, bubbles)

		trash = ET.SubElement(root, 'Trash')
		""" TOOD: add any elements that are not added yet to trash"""

		ET.dump(root)

	def createListTree(list):
		print("creating Tree of Length: "  + str(len(list)))
		tree = Tree()
		sub = tree
		for s in list:
			newtree = Tree()
			sub.bubbles.append(newtree)
			sub.bubbles[0].nuggets.append(str(s.GetIX()))
			sub = newtree
		return tree

	def compare(first, second):
		test = randint(0,3)
		# TODO: make constants for strings
		# TODO: implement this function
		# TODO: move this function to blackbox
		if(test == 0):
			return "specific"
		if(test==1):
			return "general"
		if(test==2):
			return "newtopic"

	def insert(self, item):
		if self.bubbles:
			for (x,i) in self.bubbles:
				res = compare(x,item)
				if(res == "specific"):
					# go down
					insert(x, item)
					return
				if(res == "general"):
					# insert ahead
					newtree = Tree()
					newtree.bubbles.append(x)
					self.bubbles[i] = newtree
				if(res == "newtopic"):
					# check if this is the last item, then insert and break
					if(len(self.bubbles)-1 == i):
						self.bubbles.append(item)
						return
					# else go to next
				
		else:
			self.bubbles.append(item)


def test():
	tree = Tree()
	tree.bubbles.append(Tree())
	tree.bubbles[0].nuggets.append("195")
	tree.bubbles[0].nuggets.append("9")

	tree.bubbles[0].bubbles.append(Tree())
	tree.bubbles[0].bubbles[0].nuggets.append("140")
	tree.bubbles[0].bubbles[0].bubbles.append(Tree())
	tree.bubbles[0].bubbles[0].bubbles[0].nuggets.append("142")
	tree.bubbles[0].bubbles.append(Tree())
	tree.bubbles[0].bubbles[0].nuggets.append("10")
	tree.bubbles[0].bubbles[0].nuggets.append("11")

	Tree.write([tree])

test()