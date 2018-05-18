from xml.dom import minidom
import xml.etree.ElementTree
import os


# The path where files with the hierarchies and nuggets are stored.
TREES_SOURCE_PATH = "../Corpus/Trees/FinishedTrees/FinalCorpusGoldTrees/"


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
    for filename in os.listdir(TREES_SOURCE_PATH):
        if filename.endswith(".xml"):
            print("\n====================== " + filename + " ======================")
            nugget_data = get_nuggets_from_file(filename[:-4])
            xmldoc = minidom.parse(TREES_SOURCE_PATH + filename)
            itemlist = xmldoc.getElementsByTagName('Nugget')
            for s in itemlist:
                print(nugget_data[s.attributes['id'].value][0], end=' ')

create_baseline_summary()