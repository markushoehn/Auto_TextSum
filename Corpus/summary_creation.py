from xml.dom import minidom
import xml.etree.ElementTree as ET
import os
import re


# The path where files with the hierarchies and nuggets are stored.
TREES_SOURCE_PATH = "../Corpus/Trees/FinishedTrees/FinalCorpusGoldTrees/"
SUM_PATH = "../Corpus/Trees/FinishedTrees/"


# Get all nugget information from a file with the given name.
# Returned is a dictionary of lists. The keys are the nugget IDs.
# Each list contains the information about a nugget. In the list
# with the nugget information the first item is the nugget text,
# the second the context before the nugget and the third the
# context after the nugget.
def get_nuggets_from_file(nugget_file_name):
    with open(TREES_SOURCE_PATH + nugget_file_name, encoding="utf8") as file:
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



# Create a summary for a given subtopic
def create_subtopic_summary(topic_descr):
    path = SUM_PATH + 'subtopic_summary.txt'
    with open(path, 'w', encoding='utf8') as subtopic:
        for filename in os.listdir(TREES_SOURCE_PATH):
            if filename.endswith(".xml"):
                subtopic.write("\n====================== " + filename + " ====================== Subtopic: " + topic_descr + " ======================\n")
                nugget_data = get_nuggets_from_file(filename[:-4])
                xmldoc = ET.parse(TREES_SOURCE_PATH + filename)
                root = xmldoc.getroot()
                for bubble in root.iter('Bubble'):
                    bubble_name = bubble.get('name')
                    if topic_descr in bubble_name:
                        subtopic.write(bubble_name + '\n')
                        for nugget in bubble.iter('Nugget'):
                            subtopic.write(nugget.get('id') + '\t' + nugget_data.get(nugget.get('id'))[0] + '\n')

        remove_duplicates(path)
    


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



create_baseline_summary()
create_overview_summary()
create_subtopic_summary('treatment')
