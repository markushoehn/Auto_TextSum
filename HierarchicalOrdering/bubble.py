import xml.etree.ElementTree as ET
from blackbox import compare
		
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
			print(space + "Bubbles: (" + str(len(sub.bubbles)) + ")")
			for x in sub.nuggets:
				print(space + "Nugget: " + x)
			for x in sub.bubbles:
				draw_rec(i+1, x)
			return
		draw_rec(0, self)
		print("Trash: (" + str(len(self.trash)) + ")")

	def insert(self, item):
		index = str(item.GetIX())
		if self.nuggets:
			for (x,i) in enumerate(self.nuggets):
				res = compare(x, index)
				if(res == "specific"):
					# go down
					self.bubbles.append(Bubble())
					self.bubbles[len(self.bubbles)-1].insert(item)
					return
				if(res == "general"):
					# insert ahead
					newtree = Bubble()
					newtree.nuggets = self.nuggets
					newtree.bubbles = self.bubbles
					self.nuggets = []
					self.nuggets.append(index)
					self.bubbles = []
					self.bubbles.append(newtree)
				if(res == "newtopic"):
					# check if this is the last item, then insert and break
					if(len(self.nuggets)-1 == i):
						newtree = Bubble()
						newtree.nuggets.append(index)
						self.bubbles.append(newtree)
						return
					# else go to next
		else:
			self.nuggets.append(index)


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