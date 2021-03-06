import numpy as np
from gensim.utils import simple_preprocess
import random
import nltk
from keras.preprocessing.sequence import pad_sequences

# create labeled data for the cnn
# input are only arrays of indices

# take preprocessed file with windowing applied already
window_size = 3
input_file = 'data/complete_feature_file_preprocessed_window_size_' + str(window_size) + '.txt'
# load embedding dictionary
emb_dict = np.load('data/numpy_data/embedding_dictionary300.npy').item()
data_x = []
data_y = []
vocab = {0}
pad_length = 30
with open(input_file) as f:
    for line in f:
        split_line = line.split('\t')
        label = split_line[-1]
        main_sentence = split_line[window_size + 1]
        sentences = split_line[1:(2*window_size + 2)]
        prep_sent_tokens = simple_preprocess(main_sentence)
        # only take sentences that contain a verb and have length >=5 and <= 50
        contains_verb = False
        pos_tags = nltk.pos_tag(prep_sent_tokens, tagset='universal')
        for tag in pos_tags:
            if tag[1] == 'VERB':
                contains_verb = True
                break
        if 5 <= len(prep_sent_tokens) <= 50 and contains_verb:
            all_indices = []
            for sentence in sentences:
                indices = []
                tokens = simple_preprocess(sentence)
                for tok in tokens:
                    try:
                        indices.append(emb_dict[tok])
                    except KeyError:
                        indices.append(emb_dict['__oov__'])
                vocab.update(indices)
                all_indices.append(indices)
            data_x.append(all_indices)
            if int(label) == 0:
                data_y.append((1, 0))
            else:
                data_y.append((0, 1))
print(len(data_x[0]))
data = list(zip(data_x, data_y))
vocab_size = max(vocab) + 1
random.seed(42)
random.shuffle(data)
input_len = len(data)
# convert to numpy arrays

# train_x: a list of different length vectors where each entry corresponds to a word ID
# train_y: a list of 2-component one hot vectors where the entries stand for not nugget / nugget
train_x, train_y = zip(*(data[:(input_len * 8) // 10]))
dev_x, dev_y = zip(*(data[(input_len * 8) // 10: (input_len * 9) // 10]))
test_x, test_y = zip(*(data[(input_len * 9) // 10:]))
train_x, train_y = np.array(train_x), np.array(train_y)
dev_x, dev_y = np.array(dev_x), np.array(dev_y)
test_x, test_y = np.array(test_x), np.array(test_y)

'''
# save data
np.save('data/numpy_data/x_train_cnn300.npy', train_x)
np.save('data/numpy_data/y_train_cnn300.npy', train_y)
np.save('data/numpy_data/x_dev_cnn300.npy', dev_x)
np.save('data/numpy_data/y_dev_cnn300.npy', dev_y)
np.save('data/numpy_data/x_test_cnn300.npy', test_x)
np.save('data/numpy_data/y_test_cnn300.npy', test_y)
'''