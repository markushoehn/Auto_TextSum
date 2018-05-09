import xml.etree.ElementTree
import numpy as np
from difflib import SequenceMatcher

sentences_source_files = ['\HierarchicalSum_1001.xml',
                          '\HierarchicalSum_1002.xml',
                          '\HierarchicalSum_1006.xml',
                          '\HierarchicalSum_1016.xml',
                          '\HierarchicalSum_1017.xml',
                          '\HierarchicalSum_1029.xml',
                          '\HierarchicalSum_1030.xml',
                          '\HierarchicalSum_1035.xml',
                          '\HierarchicalSum_1042.xml',
                          '\HierarchicalSum_1044.xml']
nugget_source_files = ['\Topic_1001_alternative ADHD treatments.txt',
                       '\Topic_1002_cellphone_for_12_years_old_kid.txt',
                       '\Topic_1006_discipline_issues_in_elementary_school.txt',
                       '\Topic_1016_sleep_problems_in_preschool_children.txt',
                       '\Topic_1017_student_loans.txt',
                       '\Topic_1029_parents_of_kids_doing_drugs.txt',
                       '\Topic_1030_school_punishment_policy.txt',
                       '\Topic_1035_kids_with_depression.txt',
                       '\Topic_1042_parents_concerns_about_religious_classes_at_school.txt',
                       "\Topic_1044_parents_deal_with_children's_obesity.txt"]

sentences_source_path = '..\Corpus\SourceDocuments'
nugget_source_path = '..\Corpus\Trees\Input'

nugget_ratios = np.zeros(10)
number_full_sentence_nuggets = np.zeros(10)
full_sentence_nuggets_ratio = np.zeros(10)

for i in range(10):
    xml_tree = xml.etree.ElementTree.parse(sentences_source_path + sentences_source_files[i])
    root = xml_tree.getroot()
    # save all sentences in a string and save the number of sentences
    all_sentences = ''
    sentences_list = []
    number_sentences = 0
    for s in root.iter('s'):
        # ignore unknown unicode characters
        sentence_text = s.find('content').text.encode('ascii', 'ignore').decode('ascii')
        all_sentences += sentence_text + '\n'
        sentences_list.append(sentence_text)
        number_sentences += 1

    nuggets_file = open(nugget_source_path + nugget_source_files[i], 'r')
    nuggets_string = nuggets_file.read()
    nuggets_list = nuggets_string.split('\n')
    number_nuggets = len(nuggets_list) - 1
    for j in range(number_nuggets):
        line = nuggets_list[j].split('\t')
        # replace nugget list entry by actual nugget
        if len(line) > 1:
            nuggets_list[j] = line[1]
    # save ration between number of nuggets and number of sentences
    nugget_ratios[i] = number_nuggets / number_sentences
    # calculate number of nuggets which consists of a full sentence
    for k in range(number_sentences):
        for n in range(number_nuggets):
            # check if sentences match at least 95 percent
            if SequenceMatcher(None, sentences_list[k], nuggets_list[n]).ratio() > 0.95:
                number_full_sentence_nuggets[i] += 1
    # save ratio of full sentence nuggets to all nuggets
    full_sentence_nuggets_ratio[i] = number_full_sentence_nuggets[i] / number_nuggets

print('Sentences nugget ratios: ', nugget_ratios, '\nMean of ratios: ', np.mean(nugget_ratios))
print('Ratios of full sentences nuggets to all nuggets: ', full_sentence_nuggets_ratio,
      '\nMean of ratios: ', np.mean(full_sentence_nuggets_ratio))
