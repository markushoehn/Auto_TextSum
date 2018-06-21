from xml.dom import minidom
import xml.etree.ElementTree
import os
import math
import re


# The path where files with the nuggets are stored.
NUGGETS_SOURCE_PATH = "../Corpus/Trees/FinishedTrees/FinalCorpusGoldTrees/"
# The path where files with the hierarchies are stored.
HIERARCHIES_SOURCE_PATH = "../Corpus/Trees/FinishedTrees/FinalCorpusGoldTrees/"
# True if the test data with the source paths from above are used. False
# if the file are used, that were created by our team in step 1 and 2 of
# the pipeline. These file do have other names than the test data files.
USING_TEST_DATA = True
# The path where the summaries are stored to.
SUMMARIES_PATH = "../Pipeline/03_final_summaries/"
# The nugget data.
NUGGET_DATA = {}


# Get all nugget information from a nugget file that matches with the given hierarchy
# file name. Returned is a dictionary of lists. The keys are the nugget IDs. Each
# list contains the information about a nugget. In the list with the nugget information
# the first item is the nugget text, the second the context before the nugget and the
# third the context after the nugget.
def get_nuggets_from_file(hierarchy_file_name):
    nugget_file_name = hierarchy_file_name[:-4]
    if not USING_TEST_DATA:
        nugget_file_name = "nuggets_" + get_file_id(hierarchy_file_name) + ".txt"
    with open(NUGGETS_SOURCE_PATH + nugget_file_name, encoding="utf8") as file:
        global NUGGET_DATA
        NUGGET_DATA = {}
        for nugget in file.read().splitlines():
            data = nugget.split("\t")
            NUGGET_DATA[data[0]] = data[1:]


# Returns the file ID for the given hierarchy file name.
def get_file_id(hierarchy_file_name):
    if USING_TEST_DATA:
        return hierarchy_file_name[:4]
    else:
        return hierarchy_file_name[6:-4]


# Create a simple baseline summary by just copy-pasting the sentences that belong to
# the nugget IDs in the hierarchies. All important nuggets are used for this summary.
# The sentences are taken in the order like in a depth-first search. This matches with
# a realistic summarization style were the general information are elaborated more
# and more specific before switching to the next sub topic.
def create_complete_overview_summary():
    for filename in os.listdir(HIERARCHIES_SOURCE_PATH):
        if filename.endswith(".xml"):
            print("\n====================== " + filename + " ======================")
            get_nuggets_from_file(filename)
            xmldoc = minidom.parse(HIERARCHIES_SOURCE_PATH + filename)
            itemlist = xmldoc.getElementsByTagName('Nugget')
            summary_file = open(SUMMARIES_PATH + "summary_" + get_file_id(filename) + ".txt", "w", encoding='utf-8')
            summary_file.write("Summary of document file " + filename + "\n\n")
            for i in range(0, len(itemlist)):
                nugget = NUGGET_DATA[itemlist[i].attributes['id'].value][0]
                summary_file.write(nugget + "\n" if i < len(itemlist) - 1 else nugget)
                print(nugget, end=' ')
            summary_file.close()


# Create a simple baseline summary by just copy-pasting the sentences that belong to
# the nugget IDs in the hierarchies. The maximal amount of sentences and words requested
# for this summary are given as parameter. The sentences are taken from the top part of
# the hierarchy (which means a depth-first search is applied to the tree were the
# nuggets of the bottom part are cut off to reach the requested amount of sentences and
# words).
def create_overview_summary(max_amount_of_sentences = math.inf, max_amount_of_words = math.inf, max_amount_of_chars = math.inf):
    for filename in os.listdir(HIERARCHIES_SOURCE_PATH):
        if filename.endswith(".xml"):
            print("\n====================== " + filename + " ======================")
            xml_content = xml.etree.ElementTree.parse(HIERARCHIES_SOURCE_PATH + filename).getroot()
            get_nuggets_from_file(filename)

            first_layer_of_bubbles = xml_content.findall('Bubble')
            sentences_tree, amount_of_sentences, amount_of_words, amount_of_chars = get_bubbles_and_nuggets(first_layer_of_bubbles, max_amount_of_sentences, max_amount_of_words, max_amount_of_chars)  # The bubbles and their direct nuggets of the current layer of the xml data structure.

            print("\nnugget IDs: ", flatten(sentences_tree))
            print("amount of sentences: ", amount_of_sentences)
            print("amount of words: ", amount_of_words)
            print("amount of characters: ", amount_of_chars, "\n")
            summary_file = open(SUMMARIES_PATH + "summary_" + get_file_id(filename) + ".txt", "w", encoding='utf-8')
            summary_file.write("Summary of document file " + filename + "\n\n")
            list_of_nugget_ids = flatten(sentences_tree)
            for i in range(0, len(list_of_nugget_ids)):
                nugget = NUGGET_DATA[list_of_nugget_ids[i]][0]
                summary_file.write(nugget + "\n" if i < len(list_of_nugget_ids) - 1 else nugget)
                print(nugget, end=' ')
            summary_file.close()


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
        new_required_sentences = required_amount_of_sentences - amount_of_sentences
        new_required_words = required_amount_of_words - amount_of_words
        new_required_chars = required_amount_of_chars - amount_of_chars
        next_layer, next_layer_sentences_amount, next_layer_words_amount, next_layer_chars_amount = get_bubbles_and_nuggets(bubble.findall('Bubble'), new_required_sentences, new_required_words, new_required_chars)
        if next_layer != []:
            nuggets_tree.append([nuggets, next_layer])
        else:
            nuggets_tree.append([nuggets])
        amount_of_sentences += next_layer_sentences_amount
        amount_of_words += next_layer_words_amount
        amount_of_chars += next_layer_chars_amount
    return nuggets_tree, amount_of_sentences, amount_of_words, amount_of_chars


# Create a overview summary by selecting each bubble the shortest sentence
# until the maximal amount of characters is reached. This is done to get
# as much information into the summary as possible. The bubbles are
# traversed in a way that the bubbles, which are the roots of the largest
# trees are used first.
def create_overview_summary_2(max_amount_of_chars):
    for filename in os.listdir(HIERARCHIES_SOURCE_PATH):
        if filename.endswith(".xml"):
            print("\n====================== " + filename + " ======================")
            xml_content = xml.etree.ElementTree.parse(HIERARCHIES_SOURCE_PATH + filename).getroot()
            get_nuggets_from_file(filename)
            first_sentence, first_length = first(xml_content)
            sorted_list = getBubblesSortedByTreeSize(xml_content.findall('Bubble'))
            list_of_nugget_ids = []
            amount_of_chars = first_length
            for bubble in sorted_list:
                shortest_nugget, shortest_nugget_size = getShortestNugget(bubble)
                if amount_of_chars + shortest_nugget_size <= max_amount_of_chars:
                    amount_of_chars += shortest_nugget_size
                    list_of_nugget_ids.append(shortest_nugget)

            print("\nnugget IDs: ", list_of_nugget_ids)
            print("amount of sentences: ", len(list_of_nugget_ids))
            # print("amount of words: ", amount_of_words)
            print("amount of characters: ", amount_of_chars, "\n")
            with open(SUMMARIES_PATH + "summary_" + get_file_id(filename) + ".txt", "w", encoding='utf-8') as summary_file:
                summary_file.write("Summary of document file " + filename + "\n\n")
                if(first_sentence != None):
                    summary_file.write(first_sentence + '\n')
                for i in range(0, len(list_of_nugget_ids)):
                    nugget = NUGGET_DATA[list_of_nugget_ids[i]][0]
                    summary_file.write(nugget + "\n" if i < len(list_of_nugget_ids) - 1 else nugget)
                    print(nugget, end=' ')
            



def first(content):
    possible_sentences = list()
    length = 0

    for nugget in content.iter('Nugget'):
        sentence = NUGGET_DATA[nugget.get('id')][0]
        if('is a ' in sentence or 'is an ' in sentence):
            possible_sentences.append(sentence)

    print(possible_sentences)
    if(len(possible_sentences) >= 1):
        first_sentence = possible_sentences[0]
        length = len(first_sentence)
    else:
        first_sentence = None
    print(first_sentence)
    return first_sentence, length
    

# Select from the given bubble the shortest nugget (sentence).
def getShortestNugget(bubble):
    shortest_nugget_id = None
    shortest_nugget_size = math.inf
    for nugget in bubble.findall('Nugget'):
        size = len(NUGGET_DATA[nugget.get("id")][0])
        if size < shortest_nugget_size:
            shortest_nugget_id = nugget.get("id")
            shortest_nugget_size = size
    return shortest_nugget_id, shortest_nugget_size


# Sort the bubbles at the root layer in such an order that the
# bubbles which are the root of the largest trees are first
# in the list.
def getBubblesSortedByTreeSize(list_of_bubbles):
    sorted_list = []
    for bubble in list_of_bubbles:
        amount_of_nuggets = len(bubble.findall('Nugget'))
        list_of_sub_bubbles = bubble.findall('Bubble')
        while list_of_sub_bubbles != []:
            sub_bubble = list_of_sub_bubbles.pop()
            amount_of_nuggets += len(sub_bubble.findall('Nugget'))
            list_of_sub_bubbles.extend(sub_bubble.findall('Bubble'))
        sorted_list.append((amount_of_nuggets, bubble))
    sorted_list.sort(key = lambda x : x[0], reverse = True)
    return [x for (y,x) in sorted_list]



USING_TEST_DATA = False
NUGGETS_SOURCE_PATH = "../Pipeline/01_selected_nuggets/"
HIERARCHIES_SOURCE_PATH = "../Pipeline/02_hierarchical_trees/"
# create_complete_overview_summary()
#create_overview_summary(max_amount_of_chars = 600)
create_overview_summary_2(max_amount_of_chars = 600)
