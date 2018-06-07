import xml.etree.ElementTree as ET
from blackbox import compare, which, SENTENCE_SPECIFIC, SENTENCE_GENERAL, SENTENCE_SIMILAR
		
class Bubble(object):
	""" tree class for bubbles and nuggets and trash """
	def __init__(self):
		super(Bubble, self).__init__()
		self.nuggets = []
		self.bubbles = []
		self.trash = []

	def write(trees):
		root = ET.Element('root')

		""" TOOD: should add Nuggets and Bubbles objects individually"""
		def traverse(root, sub):
			if type(sub) is Bubble:
				for n in sub.nuggets:
					index = str(n.GetIX())
					ET.SubElement(root, 'Nugget', id=index)
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
		tree = Bubble()
		sub = tree
		for s in list:
			newtree = Bubble()
			sub.bubbles.append(newtree)
			sub.bubbles[0].nuggets.append(str(s.GetIX()))
			sub = newtree
		return tree

	def draw(self):
		print("Tree:")
		def draw_rec(i, sub):
			space = (i * "  ")
			for x in sub.nuggets:
				print(space + "Nugget: " + str(x.GetIX()))
			print(space + "Bubbles: (" + str(len(sub.bubbles)) + ")")
			for x in sub.bubbles:
				draw_rec(i+1, x)
			return
		draw_rec(0, self)
		print("Trash: (" + str(len(self.trash)) + ")")

	def insert(self, item):
		if self.nuggets:
			res = compare(item, self.nuggets)
			if(res == SENTENCE_SPECIFIC):
				# go down
				if self.bubbles:
					num = which(self.bubbles, item)
					if(num >= 0):
						self.bubbles[num].insert(item)
						return
				newtree = Bubble()
				newtree.nuggets.append(item)
				self.bubbles.append(newtree)
			if(res == SENTENCE_GENERAL):
				# insert ahead
				newtree = Bubble()
				newtree.nuggets = self.nuggets
				newtree.bubbles = self.bubbles
				self.nuggets = []
				self.nuggets.append(item)
				self.bubbles = []
				self.bubbles.append(newtree)
			if(res == SENTENCE_SIMILAR):
				self.nuggets.append(item)
		else:
			self.nuggets.append(item)


def test():
	tree = Bubble()
	tree.bubbles.append(Bubble())
	tree.bubbles[0].nuggets.append("195")
	tree.bubbles[0].nuggets.append("9")

	tree.bubbles[0].bubbles.append(Bubble())
	tree.bubbles[0].bubbles[0].nuggets.append("140")
	tree.bubbles[0].bubbles[0].bubbles.append(Bubble())
	tree.bubbles[0].bubbles[0].bubbles[0].nuggets.append("142")
	tree.bubbles[0].bubbles.append(Bubble())
	tree.bubbles[0].bubbles[0].nuggets.append("10")
	tree.bubbles[0].bubbles[0].nuggets.append("11")

	Tree.write([tree])

def main():
	print("Wrtiing demo tree:")
	test()

if __name__ == "__main__":
    main()