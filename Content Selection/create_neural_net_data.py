import numpy as np
import random


# create data for neural net and save as numpy arrays

# METHOD FOR AVERAGING THE WORD EMBEDDINGS OF A SENTENCE


def average_embedding(sentence):
    # split into words by spaces
    word_list = sentence.split(' ')
    # save sentence length
    sentence_length = len(word_list)
    # initial embedding matrix (gets averaged later on along axis 0, e.h. along the single word embeddings)
    embeddings = np.zeros((sentence_length, embedding_size))
    # iterate over words
    for word_index in range(sentence_length):
        try:
            embeddings[word_index] = embedding_matrix[int(embedding_dict[word_list[word_index].lower()])]
        except KeyError:
            # handle out of vocabulary words (use oov embedding vector)
            embeddings[word_index] = embedding_matrix[int(embedding_dict['__oov__'])]
    # return mean of embeddings
    return np.mean(embeddings, axis=0)


# specify window size and embedding size
k = 5
embedding_size = 300
# load preprocessed data
data_file = open('data/complete_feature_file_preprocessed_window_size_' + str(k) + '.txt', 'r')
data_lines = data_file.read().split('\n')

# create list of labeled sentences (list of (list, label))
labeled_sentences = []
id_list = []
for line in data_lines:
    line_split = line.split('\t')
    labeled_sentences.append([line_split[1:(2*k+2)], line_split[(2*k+2)]])
    id_list.append(line_split[0])
# shuffle data
random.seed(42)
random.shuffle(labeled_sentences)
random.seed(42)
random.shuffle(id_list)

# split in training and test data
train_test_split = 2/3
splitline = int(len(labeled_sentences) * train_test_split)
labeled_train = labeled_sentences[:splitline]
labeled_test = labeled_sentences[splitline:]
id_list_train = id_list[:splitline]
id_list_test = id_list[splitline:]
# create numpy placeholders for training and testing data
x_train = np.zeros((len(labeled_train), (2*k + 1)*embedding_size))
y_train = np.zeros((len(labeled_train), 2))
x_test = np.zeros((len(labeled_test), (2*k + 1)*embedding_size))
y_test = np.zeros((len(labeled_test), 2))

# load embedding matrix and dictionary
embedding_matrix = np.load('data/numpy_data/embedding_matrix300.npy')
embedding_dict = np.load('data/numpy_data/embedding_dictionary300.npy').item()


# fill training data
for i in range(len(labeled_train)):
    # loop over sentences
    for j in range(2*k + 1):
        # concatenate the averaged sentence embeddings
        x_train[i][j*embedding_size:(j+1)*embedding_size] = average_embedding(labeled_train[i][0][j])
    # get label
    label = labeled_train[i][1]
    # create one-hot vector for y data
    if label == '0':
        y_train[i][0] = 1
    else:
        if label == '1':
            y_train[i][1] = 1
        else:
            print('LABEL ERROR')

# fill testing data
for i in range(len(labeled_test)):
    # loop over sentences
    for j in range(2 * k + 1):
        # concatenate the averaged sentence embeddings
        x_test[i][j*embedding_size:(j+1)*embedding_size] = average_embedding(labeled_test[i][0][j])
    # get label
    label = labeled_test[i][1]
    # create one-hot vector for y data
    if label == '0':
        y_test[i][0] = 1
    else:
        if label == '1':
            y_test[i][1] = 1
        else:
            print('LABEL ERROR')

# save training and testing data as numpy arrays
np.save('data/numpy_data/x_train_wsize_' + str(k) + '_embsize_' + str(embedding_size) + '.npy', x_train)
np.save('data/numpy_data/y_train_wsize_' + str(k) + '_embsize_' + str(embedding_size) + '.npy', y_train)
np.save('data/numpy_data/x_test_wsize_' + str(k) + '_embsize_' + str(embedding_size) + '.npy', x_test)
np.save('data/numpy_data/y_test_wsize_' + str(k) + '_embsize_' + str(embedding_size) + '.npy', y_test)
np.save('id_list_train', id_list_train)
np.save('id_list_test', id_list_test)
