import numpy as np
from gensim.utils import simple_preprocess
import random
from keras.preprocessing.sequence import pad_sequences

# take raw sentences
input_file = 'data/labeled_data_complete.txt'
# load embedding dictionary
emb_dict = np.load('data/embedding_dictionary300.npy').item()
data_x = []
data_y = []
vocab = {0}
pad_length = 50
with open(input_file) as f:
    for line in f:
        sent_id, sentence, label = line.split('\t')
        prep_sent_tokens = simple_preprocess(sentence)
        indices = []
        for tok in prep_sent_tokens:
            try:
                indices.append(emb_dict[tok])
            except KeyError:
                indices.append(emb_dict['__oov__'])
        if len(indices) > 0:
            data_x.append(indices)
            vocab.update(indices)
            if int(label) == 0:
                data_y.append((1, 0))
            else:
                data_y.append((0, 1))
data_x = pad_sequences(data_x, maxlen=pad_length)
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

# save data
np.save('data/numpy_data/x_train_cnn300.npy', train_x)
np.save('data/numpy_data/y_train_cnn300.npy', train_y)
np.save('data/numpy_data/x_dev_cnn300.npy', dev_x)
np.save('data/numpy_data/y_dev_cnn300.npy', dev_y)
np.save('data/numpy_data/x_test_cnn300.npy', test_x)
np.save('data/numpy_data/y_test_cnn300.npy', test_y)