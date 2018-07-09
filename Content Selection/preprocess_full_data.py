from gensim.utils import simple_preprocess

stopword_file = open('data/stopwords.txt', 'r')
stopword_list = stopword_file.read().split('\n')

raw_file = open('data/labeled_data_complete.txt', 'r')
raw_lines = raw_file.read().split('\n')

new_file = open('data/labeled_data_complete_preprocessed.txt', mode='a')

for line in raw_lines:
    split_line = line.split('\t')
    id = split_line[0]
    sentence_raw = split_line[1]
    new_sentence_tokens = simple_preprocess(sentence_raw)
    new_sentence = ' '.join([token for token in new_sentence_tokens if token not in stopword_list])
    new_file.write(id + '\t' + new_sentence + '\n')