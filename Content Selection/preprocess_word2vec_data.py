import numpy as np
import gensim


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
        if average_embeddings(line_x, gensim_model, vector_dim) is not None:
            not_none_count += 1
            ids = line_id.split('/')
            id_data[line_number] = [int(ids[0]), int(ids[1])]
            x_data[line_number] = average_embeddings(line_x, gensim_model, vector_dim)
            y_temp = np.zeros(2)
            y_temp[int(line_y)] = 1
            y_data[line_number] = y_temp
            # fill dictionary with complete line and id as key
            dictionary[line_id] = text_lines[line_number]
        else:
            remove_indices.append(line_number)
    # delete empty entries
    print(data_size, not_none_count)
    id_data = np.delete(id_data, remove_indices, axis=0)
    x_data = np.delete(x_data, remove_indices, axis=0)
    y_data = np.delete(y_data, remove_indices, axis=0)
    print(id_data.shape, x_data.shape, y_data.shape)
    return id_data, x_data, y_data, dictionary


# load model
model = gensim.models.Word2Vec.load('data/word2vec_embeddings.vec')
vec_dim = 100
# load data
id_train, x_train, y_train, dict1 = load_data('data/nugget_metdata_results/data_train.txt', model, vec_dim)
id_test, x_test, y_test, dict2 = load_data('data/nugget_metdata_results/data_test.txt', model, vec_dim)
dict1.update(dict2)
# save arrays
np.save('data/numpy_data/id_train2.npy', id_train)
np.save('data/numpy_data/x_train2.npy', x_train)
np.save('data/numpy_data/y_train2.npy', y_train)
np.save('data/numpy_data/id_test2.npy', id_test)
np.save('data/numpy_data/x_test2.npy', x_test)
np.save('data/numpy_data/y_test2.npy', y_test)
np.save('data/numpy_data/dictionary2.npy', dict1)
