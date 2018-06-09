import numpy as np
import gensim
import operator


def average_embeddings(sentence, gensim_model, vector_dim):
    # simple preprocess sentence
    sentence_tokens_before_stopwords = gensim.utils.simple_preprocess(sentence)
    # remove stopwords
    stop_word_file = open('data/stopwords.txt', 'r')
    stopword_list = stop_word_file.read().split('\n')
    sentence_tokens = [token for token in sentence_tokens_before_stopwords if token not in stopword_list]
    sentence_length = len(sentence_tokens)
    # check if there are words left
    if sentence_length == 0:
        return
    # create token vectors
    token_vectors = np.zeros((sentence_length, vector_dim))
    for j in range(sentence_length):
        token_vectors[j] = gensim_model.wv[sentence_tokens[j]]
    # return average embeddings
    return np.mean(token_vectors, axis=0)


def load_data(path, gensim_model, vector_dim):
    # create empty dictionary
    dictionary = {}
    file = open(path, 'r')
    raw_text = file.read()
    text_lines = raw_text.split('\n')
    data_size = len(text_lines)
    # create numpy arrays for ids, x data, y data
    id_data = np.empty((data_size, 2))
    x_data = np.empty((data_size, vector_dim))
    y_data = np.empty((data_size, 2))
    not_none_count = 0
    remove_indices = []
    for line_number in range(data_size):
        print(line_number, 'of', data_size)
        line_sep = text_lines[line_number].split('\t')
        line_id = line_sep[0]
        line_x = line_sep[1]
        line_y = line_sep[2]
        # check if there is actual data
        av_emb = average_embeddings(line_x, gensim_model, vector_dim)
        if av_emb is not None:
            not_none_count += 1
            ids = line_id.split('/')
            id_data[line_number] = [int(ids[0]), int(ids[1])]
            x_data[line_number] = av_emb
            y_temp = np.zeros(2)
            y_temp[int(line_y)] = 1
            y_data[line_number] = y_temp
            # fill dictionary with complete line and id as key
            dictionary[line_id] = text_lines[line_number]
        else:
            remove_indices.append(line_number)
    # delete empty entries
    id_data = np.delete(id_data, remove_indices, axis=0)
    x_data = np.delete(x_data, remove_indices, axis=0)
    y_data = np.delete(y_data, remove_indices, axis=0)
    return id_data, x_data, y_data, dictionary



# load model
model_path = 'data/word2vec_embeddings_dim100_window5.vec'
model = gensim.models.Word2Vec.load(model_path)
vec_dim = 100
# load data
id_train, x_train, y_train, dict1 = load_data('data/nugget_metdata_results/data_train.txt', model, vec_dim)
id_test, x_test, y_test, dict2 = load_data('data/nugget_metdata_results/data_test.txt', model, vec_dim)
dict1.update(dict2)
# save arrays
# np.save('data/numpy_data/id_train.npy', id_train)
####np.save('data/numpy_data/x_train100_5.npy', x_train)
###np.save('data/numpy_data/y_train100_5.npy', y_train)
# np.save('data/numpy_data/id_test.npy', id_test)
###np.save('data/numpy_data/x_test100_5.npy', x_test)
###np.save('data/numpy_data/y_test100_5.npy', y_test)
# np.save('data/numpy_data/dictionary.npy', dict1)


'''
full_file = open('data/nugget_metdata_results/data_labeled_complete.txt', 'r')
full_text_list = full_file.read().split('\n')
pos_labels_list = [line.split('\t')[1] for line in full_text_list if int(line.split('\t')[2]) == 1]
neg_labels_list = [line.split('\t')[1] for line in full_text_list if int(line.split('\t')[2]) == 0]

stop_word_file = open('data/stopwords.txt', 'r')
stopword_list = stop_word_file.read().split('\n')

# simple preprocess and remove stopwords for positive labels
for i in range(len(pos_labels_list)):
    line_tokens = gensim.utils.simple_preprocess(pos_labels_list[i])
    line_tokens_wo_sw = [token for token in line_tokens if token not in stopword_list]
    pos_labels_list[i] = ' '.join(line_tokens_wo_sw)

# create word count for positive label words
all_pos_words = ' '.join(pos_labels_list)
all_pos_words_list = all_pos_words.split(' ')
positive_dictionary = {}
for word in all_pos_words_list:
    if word in positive_dictionary:
        positive_dictionary[word] += 1 / len(all_pos_words_list)
    else:
        positive_dictionary[word] = 1 / len(all_pos_words_list)
# create ordered list
positive_words_sorted = sorted(positive_dictionary.items(), key=operator.itemgetter(1))
# reverse list
positive_words_sorted = list(reversed(positive_words_sorted))

# simple preprocess and remove stopwords for negative labels
for i in range(len(neg_labels_list)):
    line_tokens = gensim.utils.simple_preprocess(neg_labels_list[i])
    line_tokens_wo_sw = [token for token in line_tokens if token not in stopword_list]
    neg_labels_list[i] = ' '.join(line_tokens_wo_sw)

# create word count for negative label words
all_neg_words = ' '.join(neg_labels_list)
all_neg_words_list = all_neg_words.split(' ')
negative_dictionary = {}
for word in all_neg_words_list:
    if word in negative_dictionary:
        negative_dictionary[word] += 1 / len(all_neg_words_list)
    else:
        negative_dictionary[word] = 1 / len(all_neg_words_list)
# create ordered list
negative_words_sorted = sorted(negative_dictionary.items(), key=operator.itemgetter(1))
# reverse list
negative_words_sorted = list(reversed(negative_words_sorted))


# idee: statt mitteln der embedding vektoren (oben):
# gewichtung nach relativer häufigkeit in positiven labels bzw nach
# verhältnis von pos zu neg häufigkeit
# problem: zu starke anpassung an trainingsdaten? bzw. an 10 dokumente
min_pos_frequency = 0.0001
ratio_threshold = 2

for word in positive_dictionary.keys():
    if word in negative_dictionary.keys():
        ratio = positive_dictionary[word] / negative_dictionary[word]
        if positive_dictionary[word] > min_pos_frequency and ratio > ratio_threshold:
            print(word, 'pos frequency:', positive_dictionary[word],
                  'neg frequency:', negative_dictionary[word],
                  'ratio:', ratio)
'''
