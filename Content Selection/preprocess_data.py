import xml.etree.ElementTree

complete_labeled_data_file = open('data/nugget_metdata_results/data_labeled_complete.txt', 'r')
complete_list = complete_labeled_data_file.readlines()
number_instances = len(complete_list)

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

sentences_source_path = '..\Corpus\SourceDocuments'

instance_count = 0

new_file = open('data/labeled_data_complete_new.txt', 'a')

for i in range(10):



    xml_tree = xml.etree.ElementTree.parse(sentences_source_path + sentences_source_files[i])
    root = xml_tree.getroot()
    doc_count = 0
    for doc in root.iter('document'):
        # get number of sentences in doc
        for content in doc.iter('content'):
            original_line = complete_list[instance_count]
            original_line_splitted = original_line.split('\t')

            # id needs to be changed
            id = original_line_splitted[0]

            id_split = id.split('/')
            new_id = id_split[0] + '/' + str(doc_count) + '/' + id_split[1]

            new_file.write('\t'.join([new_id, original_line_splitted[1], original_line_splitted[2]]))

            instance_count += 1

        doc_count += 1

print(number_instances, instance_count)
    # document count


