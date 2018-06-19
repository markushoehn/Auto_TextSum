import xml.etree.ElementTree
from gensim.utils import simple_preprocess

# create unlabeled data for all 49 topics and save it as txt files

# list of all source file paths
sentences_source_files = ['..\AutoTS_Corpus\DIP2017_source_10' + str(format(i, '02d')) + '.xml'
                          for i in range(1, 51)]

# load stopword list
stopword_file = open('data/stopwords.txt', 'r')
stopword_list = stopword_file.read().split('\n')


def preprocess(sentence):
    sentence_tokens = simple_preprocess(sentence)
    new_sentence = ' '.join([token for token in sentence_tokens if token not in stopword_list])
    return new_sentence


for file_number in range(50, 51):
    # number 9 is missing
    if not file_number == 9:
        # open source file with xml reader
        xml_tree = xml.etree.ElementTree.parse(sentences_source_files[file_number - 1])
        root = xml_tree.getroot()
        # create new file for raw and preprocessed data
        raw_file = open('data/unlabeled/raw/unlabeled_raw_10' + str(format(file_number, '02d')) + '.txt', 'a')
        preprocessed_file = open('data/unlabeled/preprocessed/unlabeled_preprocessed_10'
                                 + str(format(file_number, '02d')) + '.txt', 'a')
        content_id = '10' + str(str(format(file_number, '02d')))
        doc_count = 0
        sentence_count = 0
        # iterate over all documents
        for doc in root.iter('document'):
            doc_count += 1
            doc_id = str(doc_count)
            # iterate over sentences in document
            for content in doc.iter('content'):
                sentence_count += 1
                sentence_id = str(sentence_count)
                sentence_raw = content.text.encode('ascii', 'ignore').decode('ascii')
                sentence_preprocessed = preprocess(sentence_raw)
                # create full id
                full_id = content_id + '/' + doc_id + '/' + sentence_id
                # write on files
                if doc_count == 1 and sentence_count == 1:
                    raw_file.write(full_id + '\t' + sentence_raw)
                    preprocessed_file.write(full_id + '\t' + sentence_preprocessed)
                else:
                    raw_file.write('\n' + full_id + '\t' + sentence_raw)
                    preprocessed_file.write('\n' + full_id + '\t' + sentence_preprocessed)
