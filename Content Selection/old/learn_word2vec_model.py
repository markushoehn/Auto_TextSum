from gensim.models import KeyedVectors, Word2Vec, word2vec
import gensim.utils
import os
import xml.etree.ElementTree

'''
# save data for training
source_files = os.listdir('../AutoTS_Corpus')
word2vec_file = open('data/word2vec_training_data.txt', 'w')

number_of_docs = len(source_files)
doc_count = 0

for doc in source_files:
    doc_count += 1
    print('Document', doc_count, 'out of', number_of_docs)
    xml_tree = xml.etree.ElementTree.parse('../AutoTS_Corpus/' + doc)
    root = xml_tree.getroot()
    for s in root.iter('s'):
        sentence_text = s.find('content').text.encode('ascii', 'ignore').decode('ascii')
        sentence_token_list = gensim.utils.simple_preprocess(sentence_text)
        preprocessed_text = ' '.join(sentence_token_list)
        word2vec_file.write(preprocessed_text + '\n')
'''

'''
sentences = word2vec.LineSentence('data/word2vec_training_data.txt')
model = Word2Vec(sentences, size=100, window=4, min_count=1)
model.save('data/word2vec_embeddings.vec')
'''

model = Word2Vec.load('data/word2vec_embeddings.vec')
print(model.wv['constitutional'])