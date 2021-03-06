import xml.etree.ElementTree as ET
import xml.dom.minidom
from blackbox import SENTENCE_SPECIFIC, SENTENCE_GENERAL, SENTENCE_SIMILAR

class Bubble(object):
	""" tree class for bubbles and nuggets and trash """
	def __init__(self):
		super(Bubble, self).__init__()
		self.nuggets = []
		self.bubbles = []
		self.trash = []

	def pretty(string):
		reparsed = xml.dom.minidom.parseString(string)
		return reparsed.toprettyxml(indent="\t")

	def write(trees, path):
		root = ET.Element('root')
		def traverse(root, sub):
			if type(sub) is Bubble:
				for n in sub.nuggets:
					index = str(n.GetIX())
					ET.SubElement(root, 'Nugget', id=index)
				for bubble in sub.bubbles:
					b = ET.SubElement(root, 'Bubble', name="")
					traverse(b, bubble)

		for bubbles in trees:
			b = ET.SubElement(root, 'Bubble', name="")
			traverse(b, bubbles)

		trash = ET.SubElement(root, 'Trash')
		string = Bubble.pretty(ET.tostring(root, encoding="unicode"))

		with open(path, 'w') as f:
			f.write(string)

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
				print(space + "Nugget: " + str(x.GetIX()) + " = " + x.GetSentence())
			print(space + "Bubbles: (" + str(len(sub.bubbles)) + ")")
			for x in sub.bubbles:
				draw_rec(i+1, x)
			return
		draw_rec(0, self)
		print("Trash: (" + str(len(self.trash)) + ")")

	def insert(self, item, blackbox):
		if self.nuggets:
			res = blackbox.compare(item, self.nuggets)
			if(res == SENTENCE_SPECIFIC):
				# go down
				if self.bubbles:
					num = blackbox.which(item, self.bubbles)
					if(num >= 0):
						self.bubbles[num].insert(item, blackbox)
						return
				temp = Bubble()
				temp.nuggets.append(item)
				self.bubbles.append(temp)
			if(res == SENTENCE_GENERAL):
				# insert ahead
				temp = Bubble()
				temp.nuggets = self.nuggets
				temp.bubbles = self.bubbles
				self.nuggets = []
				self.nuggets.append(item)
				self.bubbles = []
				self.bubbles.append(temp)
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
	print("writing demo tree:")
	test()

if __name__ == "__main__":
    main()