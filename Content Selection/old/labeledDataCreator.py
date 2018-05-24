import xml.etree.ElementTree as ET
import re
from difflib import SequenceMatcher

LABEL_NONUGGET = "__label__noNugget"
LABEL_ISNUGGET = "__label__isNugget"
LABEL_CONTAINSNUGGET =  "__label__containsNugget"

SENTENCES_SOURCE_PATH = '../Corpus/SourceDocuments'
NUGGET_SOURCE_PATH = '../Corpus/Trees/Input'
OUTPUT_NAME = "labeled_data_fastText.txt"

SENTENCES_SOURCE_FILES = ['/HierarchicalSum_1001.xml',
                          '/HierarchicalSum_1002.xml',
                          '/HierarchicalSum_1006.xml',
                          '/HierarchicalSum_1016.xml',
                          '/HierarchicalSum_1017.xml',
                          '/HierarchicalSum_1029.xml',
                          '/HierarchicalSum_1030.xml',
                          '/HierarchicalSum_1035.xml',
                          '/HierarchicalSum_1042.xml',
                          '/HierarchicalSum_1044.xml']
NUGGET_SOURCE_FILES = ['/Topic_1001_alternative ADHD treatments.txt',
                       '/Topic_1002_cellphone_for_12_years_old_kid.txt',
                       '/Topic_1006_discipline_issues_in_elementary_school.txt',
                       '/Topic_1016_sleep_problems_in_preschool_children.txt',
                       '/Topic_1017_student_loans.txt',
                       '/Topic_1029_parents_of_kids_doing_drugs.txt',
                       '/Topic_1030_school_punishment_policy.txt',
                       '/Topic_1035_kids_with_depression.txt',
                       '/Topic_1042_parents_concerns_about_religious_classes_at_school.txt',
                       "/Topic_1044_parents_deal_with_children's_obesity.txt"]

def create_fasttext_data():
    # iterate over all sentence- and their respective nugget files
    with open(OUTPUT_NAME, 'x') as labeled_data:
        for i in range(0,10):
            sentence_tree = ET.parse(SENTENCES_SOURCE_PATH + SENTENCES_SOURCE_FILES[i])
            sentence_root = sentence_tree.getroot()
            print("reading file %s" % SENTENCES_SOURCE_FILES[i])
            
            # read all sentences from the Sentences file
            for sentence in sentence_root.iter('content'):
                sentence_text = sentence.text.encode('ascii', 'ignore').decode('ascii').strip()
                nugget_found = False
                # read all nuggets from nuggets file
                with open(NUGGET_SOURCE_PATH + NUGGET_SOURCE_FILES[i], 'r') as nugget_file:
                    for line in nugget_file:
                        nugget_parts = re.split("\t", line.strip())     # reads a line from the nugget file and splits it into segments at each tab.
                                                                        # the strip() method filters out special characters like linebreaks
                        # compare sentences and nuggets for similarity
                        # similarity > 95% -> label as nugget and extract the nugget from the Sentence Sourcefile in order to ignore their tokenization
                        # additionally: put into context and label the resulting string as containing a nugget
                        if SequenceMatcher(None, sentence_text, nugget_parts[1]).ratio() > 0.95:
                            labeled_data.write(LABEL_ISNUGGET + " " + nugget_parts[1] + "\n")
                            labeled_data.write(LABEL_CONTAINSNUGGET + " " + " ".join([nugget_parts[2], nugget_parts[1], nugget_parts[3]]) + "\n")
                            nugget_found = True
                    
                    # if no corresponding nugget was found -> store as not containing a nugget
                    if not nugget_found:
                        labeled_data.write(LABEL_NONUGGET + " " + sentence_text + "\n")

create_fasttext_data()