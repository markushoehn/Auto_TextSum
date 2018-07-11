import numpy as np
from gensim.utils import simple_preprocess
import random
from keras.preprocessing.sequence import pad_sequences

# load stopword list
stopword_file = open('data/stopwords.txt', 'r')
stopword_list = stopword_file.read().split('\n')
# take raw sentences
input_file = 'data/labeled_data_complete.txt'
# load embedding dictionary
emb_dict = np.load('data/numpy_data/embedding_dictionary300_tf_idf.npy').item()
data_x = []
data_y = []
vocab = {0}
pad_length = 50
in_vocab_words = 0
out_of_vocab_words = 0
with open(input_file) as f:
    for line in f:
        full_id, sentence, label = line.split('\t')
        topic_id, doc_id, sent_id = full_id.split('/')
        prep_sent_tokens = simple_preprocess(sentence)
        # take only sentences with min 5 and max 50 tokens
        if 5 <= len(prep_sent_tokens) <= 50:
            indices = []
            tokens_without_stopwords = [token for token in prep_sent_tokens if token not in stopword_list]
            for tok in tokens_without_stopwords:
                try:
                    indices.append(emb_dict[tok + '_' + topic_id + '_' + doc_id])
                    in_vocab_words += 1
                except KeyError:
                    print(tok + '_' + topic_id + '_' + doc_id)
                    indices.append(emb_dict['__oov__'])
                    out_of_vocab_words += 1
            if len(indices) > 0:
                data_x.append(indices)
                vocab.update(indices)
                if int(label) == 0:
                    data_y.append((1, 0))
                else:
                    data_y.append((0, 1))
print('OOV rate:', out_of_vocab_words / (in_vocab_words + out_of_vocab_words))
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
np.save('data/numpy_data/x_train_cnn300_tf_idf.npy', train_x)
np.save('data/numpy_data/y_train_cnn300_tf_idf.npy', train_y)
np.save('data/numpy_data/x_dev_cnn300_tf_idf.npy', dev_x)
np.save('data/numpy_data/y_dev_cnn300_tf_idf.npy', dev_y)
np.save('data/numpy_data/x_test_cnn300_tf_idf.npy', test_x)
np.save('data/numpy_data/y_test_cnn300_tf_idf.npy', test_y)
