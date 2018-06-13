from xml.dom import minidom
import xml.etree.ElementTree
import os
import math


# The path where files with the hierarchies and nuggets are stored.
TREES_SOURCE_PATH = "../Corpus/Trees/FinishedTrees/FinalCorpusGoldTrees/"
NUGGET_DATA = {}


# Get all nugget information from a file with the given name. Returned is a dictionary
# of lists. The keys are the nugget IDs. Each list contains the information about a
# nugget. In the list with the nugget information the first item is the nugget text,
# the second the context before the nugget and the third the context after the nugget.
def get_nuggets_from_file(nugget_file_name):
    with open(TREES_SOURCE_PATH + nugget_file_name, encoding="utf8") as file:
        global NUGGET_DATA
        NUGGET_DATA = {}
        for nugget in file.read().splitlines():
            data = nugget.split("\t")
            NUGGET_DATA[data[0]] = data[1:]


# Create a simple baseline summary by just copy-pasting the sentences that belong to
# the nugget IDs in the hierarchies. All important nuggets are used for this summary.
# The sentences are taken in the order like in a depth-first search. This matches with
# a realistic summarization style were the general information are elaborated more
# and more specific before switching to the next sub topic.
def create_complete_overview_summary():
    for filename in os.listdir(TREES_SOURCE_PATH):
        if filename.endswith(".xml"):
            print("\n====================== " + filename + " ======================")
            get_nuggets_from_file(filename[:-4])
            xmldoc = minidom.parse(TREES_SOURCE_PATH + filename)
            itemlist = xmldoc.getElementsByTagName('Nugget')
            for s in itemlist:
                print(NUGGET_DATA[s.attributes['id'].value][0], end=' ')


# Create a simple baseline summary by just copy-pasting the sentences that belong to
# the nugget IDs in the hierarchies. The maximal amount of sentences and words requested
# for this summary are given as parameter. The sentences are taken from the top part of
# the hierarchy (which means a depth-first search is applied to the tree were the
# nuggets of the bottom part are cut off to reach the requested amount of sentences and
# words).
def create_overview_summary(max_amount_of_sentences = math.inf, max_amount_of_words = math.inf, max_amount_of_chars = math.inf):
    for filename in os.listdir(TREES_SOURCE_PATH):
        if filename.endswith(".xml"):
            print("\n====================== " + filename + " ======================")
            xml_content = xml.etree.ElementTree.parse(TREES_SOURCE_PATH + filename).getroot()
            get_nuggets_from_file(filename[:-4])

            first_layer_of_bubbles = xml_content.findall('Bubble')
            sentences_tree, amount_of_sentences, amount_of_words, amount_of_chars = get_bubbles_and_nuggets(first_layer_of_bubbles, max_amount_of_sentences, max_amount_of_words, max_amount_of_chars)  # The bubbles and their direct nuggets of the current layer of the xml data structure.
            #print("\nfinished tree: ", sentences_tree)
            print("\nnugget IDs: ", flatten(sentences_tree))
            print("amount of sentences: ", amount_of_sentences)
            print("amount of words: ", amount_of_words)
            print("amount of characters: ", amount_of_chars, "\n")
            #print(len(flatten(sentences_tree)), " sentences")

            for nugget_id in flatten(sentences_tree):
                print(NUGGET_DATA[nugget_id][0], end=' ')


# Flattens the given list recursively
def flatten(givenList):
    if givenList == []:
        return givenList
    if isinstance(givenList[0], list):
        return flatten(givenList[0]) + flatten(givenList[1:])
    return givenList[:1] + flatten(givenList[1:])        


# Recursively go down the hierarchy and store the IDs of the nuggets. Stop when the
# requested amount of sentences, words or characters is reached.
def get_bubbles_and_nuggets(list_of_bubbles, required_amount_of_sentences = math.inf, required_amount_of_words = math.inf, required_amount_of_chars = math.inf):
    amount_of_sentences = 0
    amount_of_words = 0
    amount_of_chars = 0
    bubbles_tree = []  # The bubbles and their direct nuggets of the current layer of the xml data structure.
    reached_amount = False
    for bubble in list_of_bubbles:
        nuggets = []
        for nugget in bubble.findall('Nugget'):
            words = len(NUGGET_DATA[nugget.get("id")][0].split())  # The amount of words of the nugget.
            chars = len(NUGGET_DATA[nugget.get("id")][0])  # The amount of characters of the nugget.
            if (amount_of_sentences == required_amount_of_sentences or
                    amount_of_words + words >= required_amount_of_words or
                    amount_of_chars + chars >= required_amount_of_chars):
                reached_amount = True
                break
            nuggets.append(nugget.get("id"))
            amount_of_sentences += 1
            amount_of_words += words
            amount_of_chars += chars
        bubbles_tree.append((bubble, nuggets))
        if reached_amount:
            break

    nuggets_tree = []
    for (bubble, nuggets) in bubbles_tree:
        # If the amount of sentences or words is already reached: Just store the already
        # extracted nugget IDs during iterating over the bubbles
        if reached_amount:
            nuggets_tree.append(nuggets)
            continue
        # Find all sub bubbles of the bubble to recursively extract the nuggets from them.
        bubbles = bubble.findall('Bubble')
        #print("-----------\nbubble name: ", bubble.get("name"))
        new_required_sentences = required_amount_of_sentences - amount_of_sentences
        new_required_words = required_amount_of_words - amount_of_words
        new_required_chars = required_amount_of_chars - amount_of_chars
        next_layer, next_layer_sentences_amount, next_layer_words_amount, next_layer_chars_amount = get_bubbles_and_nuggets(bubble.findall('Bubble'), new_required_sentences, new_required_words, new_required_chars)
        if next_layer != []:
            #print("new layer amount of sentences", next_layer_sentences_amount)
            #print("new layer amount of words", next_layer_words_amount)
            #print("new layer amount of chars", next_layer_chars_amount)
            #print("new layer added ", next_layer)
            nuggets_tree.append([nuggets, next_layer])
        else:
            #print("new layer amount of sentences", next_layer_sentences_amount)
            #print("new layer amount of words", next_layer_words_amount)
            nuggets_tree.append([nuggets])
        amount_of_sentences += next_layer_sentences_amount
        amount_of_words += next_layer_words_amount
        amount_of_chars += next_layer_chars_amount
    return nuggets_tree, amount_of_sentences, amount_of_words, amount_of_chars



#create_complete_overview_summary()
create_overview_summary(max_amount_of_chars = 600)