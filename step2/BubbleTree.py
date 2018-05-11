import xml.etree.ElementTree as ET
		
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