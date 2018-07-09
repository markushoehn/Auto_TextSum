import xml
from xml.dom import minidom
import xml.etree.ElementTree as ET
import os
import re
import math
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.kl import KLSummarizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from summa import summarizer



# The path where files with the hierarchies and nuggets are stored.
TREES_SOURCE_PATH = "../Pipeline/02_hierarchical_trees/"
NUGGET_PATH = "../Pipeline/01_selected_nuggets/"
SUM_PATH = "C:\\Users\\jojoh\\Documents\\6. Semester\\AutoTS\\Abgabe\\"


# Get all nugget information from a file with the given name.
# Returned is a dictionary of lists. The keys are the nugget IDs.
# Each list contains the information about a nugget. In the list
# with the nugget information the first item is the nugget text,
# the second the context before the nugget and the third the
# context after the nugget.
def get_nuggets_from_file(nugget_file_name):
    with open(NUGGET_PATH + "nuggets_" + nugget_file_name + ".txt", encoding="utf8") as file:
        nugget_data = {}
        for nugget in file.read().splitlines():
            data = nugget.split("\t")
            nugget_data[data[0]] = data[1:]
        return nugget_data



# Create a simple baseline summary by just copy-pasting the
# sentences that belong to the nugget IDs in the hierarchies.
def create_baseline_summary():
    with open(SUM_PATH + 'baseline_summary.txt', 'w', encoding='utf8') as summary:
        for filename in os.listdir(TREES_SOURCE_PATH):
            if filename.endswith(".xml"):
                summary.write("\n====================== " + filename + " ======================\n")
                nugget_data = get_nuggets_from_file(filename[:-4])
                xmldoc = minidom.parse(TREES_SOURCE_PATH + filename)
                itemlist = xmldoc.getElementsByTagName('Nugget')
                for s in itemlist:
                    summary.write(nugget_data[s.attributes['id'].value][0])




            # with open(TREES_SOURCE_PATH + filename, encoding="utf8") as file:
            #     hierarchy = file.read()
            #     nugget_data = get_nuggets_from_file(filename[:-4])
            #     
                # e = xml.etree.ElementTree.parse(TREES_SOURCE_PATH + filename).getroot()
                # for atype in e.findall('Nugget'):
                #     print(atype.get('id'))
            # file.close()



# Create an overview summary which uses only the top level bubbles
# and their children
# optional: use only one Nugget per Bubble (currently the first) to
# avoid repition and to get a shorter summary
def create_overview_summary():
    with open(SUM_PATH + 'overview_summary.txt', 'w', encoding='utf8') as overview:
        for filename in os.listdir(TREES_SOURCE_PATH):
            if filename.endswith(".xml"):
                overview.write("\n====================== " + filename + " ======================\n")
                nugget_data = get_nuggets_from_file(filename[:-4])
                xmldoc = ET.parse(TREES_SOURCE_PATH + filename)
                root = xmldoc.getroot()
                for child in root.findall('./Bubble/*'):
                    if(child.tag == 'Nugget' and child in root.findall('./Bubble/Nugget[1]')):
                        overview.write(child.get('id') + '\t' + nugget_data.get(child.get('id'))[0] + '\n')

                    for grandchild in child:
                        if(grandchild.tag == 'Nugget' and grandchild in root.findall('./Bubble/Bubble/Nugget[1]')):
                            overview.write(grandchild.get('id') + '\t' + nugget_data.get(grandchild.get('id'))[0] + '\n')

    


#remove all duplicate sentences from a given file
def remove_duplicates(filepath):
    filename = re.search(SUM_PATH + '(.*)\.txt', filepath)
    with open(filepath, 'r', encoding='utf8') as i:
        with open(SUM_PATH + 'duplicate_free_' + filename.group(1) + '.txt', 'w', encoding='utf8') as o:
            lines_seen = set()
            for line in i:
                if(line not in lines_seen):
                    o.write(line)
                    lines_seen.add(line)


# Create a summary using the sumy implementation of the LexRank summarizer
def create_lexrank_summary():
    for filename in os.listdir(TREES_SOURCE_PATH):
        if filename.endswith('.xml'):
            name = re.search('topic_(.*)\.xml', filename)
            input_path = create_input(name.group(1))
            with open(SUM_PATH + name.group(1) + '_LexRank_Group5.txt', 'w', encoding='utf8') as summary:
                summary.write("====================== General Summary of " + name.group(1) + " ======================\n")
                parser = PlaintextParser.from_file(input_path, Tokenizer("english"))
                summarizer = LexRankSummarizer()

                s = summarizer(parser.document, 4)

                for sentence in s:
                    summary.write(str(sentence) + '\n')



# Create a summary using the sumy implementation of the Luhn summarizer
def create_luhn_summary():
    for filename in os.listdir(TREES_SOURCE_PATH):
        if filename.endswith('.xml'):
            name = re.search('topic_(.*)\.xml', filename)
            input_path = create_input(name.group(1))
            with open(SUM_PATH + name.group(1) + '_Luhn_Group5.txt', 'w', encoding='utf8') as summary:
                summary.write("====================== General Summary of " + name.group(1) + " ======================\n")
                parser = PlaintextParser.from_file(input_path, Tokenizer("english"))
                summarizer = LuhnSummarizer()

                s = summarizer(parser.document, 3)

                for sentence in s:
                    summary.write(str(sentence) + '\n')



# Create a summary using the sumy implementation of the LSA summarizer
def create_lsa_summary():
    for filename in os.listdir(TREES_SOURCE_PATH):
        if filename.endswith('.xml'):
            name = re.search('topic_(.*)\.xml', filename)
            input_path = create_input(name.group(1))
            with open(SUM_PATH + name.group(1) + '_LSA_Group5.txt', 'w', encoding='utf8') as summary:
                summary.write("====================== General Summary of " + name.group(1) + " ======================\n")
                parser = PlaintextParser.from_file(input_path, Tokenizer("english"))
                summarizer = LsaSummarizer()

                s = summarizer(parser.document, 4)

                for sentence in s:
                    summary.write(str(sentence) + '\n')



# Create a summary using the sumy implementation of the TextRank summarizer
def create_textrank_summary(max_chars):
    for filename in os.listdir(TREES_SOURCE_PATH):
        chars = 0
        if filename.endswith('.xml'):
            name = re.search('topic_(.*)\.xml', filename)
            input_path = create_input(name.group(1))
            path = SUM_PATH + name.group(1) 
            with open(path + '_TextRank_Group5.txt', 'w', encoding='utf8') as summary:
                summary.write("====================== General Summary of " + name.group(1) + " ======================\n")
                parser = PlaintextParser.from_file(input_path, Tokenizer("english"))
                summarizer = TextRankSummarizer()

                s = summarizer(parser.document, 3)
                
                for sentence in s:
                    if (chars + len(str(sentence)) <= max_chars):
                        summary.write(str(sentence) + '\n')
                        chars += len(str(sentence))
            
            expand_textrank(name.group(1), path, max_chars, chars)




def expand_textrank(filename, sum_path, max_chars, chars):
    with open(sum_path + '_TextRank_Group5.txt', 'r', encoding='utf8') as summary:
        with open (sum_path + '_expanded_TextRank_Group5.txt', 'w', encoding='utf8') as o:
            
            for line in summary:
                o.write(line)
                
            nugget_data = get_nuggets_from_file(filename)
            xml_content = xml.etree.ElementTree.parse(TREES_SOURCE_PATH + 'topic_' + filename + '.xml').getroot()
            sorted_list = getBubblesSortedByTreeSize(xml_content.findall('Bubble'))
            for bubble in sorted_list:
                shortest_nugget, shortest_nugget_size = getShortestNugget(bubble, nugget_data)
                if(chars + shortest_nugget_size <= max_chars):
                    o.write(shortest_nugget + '\n')
                    chars += shortest_nugget_size



# Select from the given bubble the shortest nugget (sentence).
def getShortestNugget(bubble, nugget_data):
    shortest_nugget_text = None
    shortest_nugget_size = math.inf
    for nugget in bubble.findall('Nugget'):
        size = len(nugget_data.get(nugget.get("id"))[0])
        if(size < shortest_nugget_size):
            shortest_nugget_text = nugget_data.get(nugget.get("id"))[0]
            shortest_nugget_size = size
    return shortest_nugget_text, shortest_nugget_size


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
        

# Create a summary using the sumy implementation of the KL divergence summarizer
def create_kl_summary(max_chars):
    for filename in os.listdir(TREES_SOURCE_PATH):
        chars = 0
        if filename.endswith('.xml'):
            name = re.search('topic_(.*)\.xml', filename)
            input_path = create_input(name.group(1))
            length = 0
            with open(SUM_PATH + name.group(1) + '_KL_Group5.txt', 'w', encoding='utf8') as summary:
                
                summary.write("====================== General Summary of " + name.group(1) + " ======================\n")
                parser = PlaintextParser.from_file(input_path, Tokenizer("english"))
                summarizer = KLSummarizer()

                s = summarizer(parser.document, 4)                

                for sentence in s:
                    if (chars + len(str(sentence)) <= max_chars):
                        summary.write(str(sentence) + '\n')
                        chars += len(str(sentence))
                



def create_another(max_chars):
    for filename in os.listdir(TREES_SOURCE_PATH):
        chars = 0
        if filename.endswith('.xml'):
            name = re.search('topic_(.*)\.xml', filename)
            path = SUM_PATH + name.group(1) 
            input_text = ''
            nugget_data = get_nuggets_from_file(name.group(1))
            xmldoc = ET.parse(TREES_SOURCE_PATH + 'topic_' + name.group(1) + '.xml')
            root = xmldoc.getroot()
                
            for nugget in root.iter('Nugget'):
                input_text = input_text + ' ' + nugget_data.get(nugget.get('id'))[0]

            with open(path + '_Group5.txt', 'w', encoding='utf8') as summary:
                summary.write("====================== General Summary of " + name.group(1) + " ======================\n")
                s = summarizer.summarize(input_text, words = 90, split=True)
            
                for sentence in s:
                    
                    if(chars + len(sentence) <= max_chars): 
                        summary.write('\n' + sentence)
                        chars +=  len(sentence)

            #expand_summ(name.group(1), path, max_chars, chars)




def expand_summ(filename, sum_path, max_chars, chars):
    with open(sum_path + '_Summ_Group5.txt', 'r', encoding='utf8') as summary:
        with open (sum_path + '_expanded_Summ_Group5.txt', 'w', encoding='utf8') as o:
            
            for line in summary:
                o.write(line)
                
            nugget_data = get_nuggets_from_file(filename)
            xml_content = xml.etree.ElementTree.parse(TREES_SOURCE_PATH + 'topic_' + filename + '.xml').getroot()
            sorted_list = getBubblesSortedByTreeSize(xml_content.findall('Bubble'))
            for bubble in sorted_list:
                shortest_nugget, shortest_nugget_size = getShortestNugget(bubble, nugget_data)
                if(chars + shortest_nugget_size <= max_chars):
                    o.write('\n' + shortest_nugget)
                    chars += shortest_nugget_size

    




# helper
def create_input(filename):
    path = SUM_PATH + 'input.txt'
    with open(path, 'w', encoding='utf8') as i:
        input_text = ''
        nugget_data = get_nuggets_from_file(filename)
        xmldoc = ET.parse(TREES_SOURCE_PATH + 'topic_' + filename + '.xml')
        root = xmldoc.getroot()
                
        for nugget in root.iter('Nugget'):
            input_text = input_text + ' ' + nugget_data.get(nugget.get('id'))[0]
            

        i.write(input_text)
        
        return path
        


   
                


#create_baseline_summary()
#create_overview_summary()
#create_gensim_summary()
#create_lexrank_summary()
#create_luhn_summary()
#create_lsa_summary()
#create_textrank_summary(600)
#create_kl_summary(600)
create_another(600)

