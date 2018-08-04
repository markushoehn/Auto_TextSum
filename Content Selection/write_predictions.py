import numpy as np
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import *
from gensim.utils import simple_preprocess

# load stopword list
stopword_file = open('data/stopwords.txt', 'r')
stopword_list = stopword_file.read().split('\n')


def write_predictions(topic_number):
    emb_dict = np.load('data/numpy_data/embedding_dictionary300.npy').item()
    emb_matrix = np.load('data/numpy_data/embedding_matrix300.npy')
    embedding_dims = 300
    data_x = []
    id_list = []
    sentence_dict = {}
    vocab = {0}
    pad_length = 50
    source_txt = 'data/unlabeled/raw/unlabeled_raw_' + str(topic_number) + '.txt'
    with open(source_txt) as f:
        for line in f:
            sent_id, sentence = line.split('\t')
            sentence_dict[sent_id] = sentence
            prep_sent_tokens = simple_preprocess(sentence)
            # only take sentence if there are between 5 and 50
            if 5 <= len(prep_sent_tokens) <= 50:
                indices = []
                for tok in prep_sent_tokens:
                    try:
                        indices.append(emb_dict[tok])
                    except KeyError:
                        indices.append(emb_dict['__oov__'])
                if len(indices) > 0:
                    data_x.append(indices)
                    vocab.update(indices)
                    id_list.append(sent_id)
    data_x = pad_sequences(data_x, maxlen=pad_length)
    vocab_size = max(vocab) + 1
    input_len = len(data_x)
    # convert to numpy array
    data_x = np.array(data_x)

    # hyperparameters
    number_conv_layers, number_filters, kernel_sizes, acts = 2, [47, 42], [6, 6], ['relu', 'relu']
    model_path = 'best_model_cnn.hdf5'

    # specify cnn model
    model = Sequential()
    model.add(Embedding(vocab_size, embedding_dims, weights=[emb_matrix], input_length=pad_length))
    model.add(BatchNormalization())
    for i in range(number_conv_layers):
        model.add(Conv1D(filters=number_filters[i], kernel_size=kernel_sizes[i]))
        model.add(Activation(acts[i]))
    model.add(GlobalMaxPool1D())
    model.add(Dense(units=2))
    model.add(Activation('softmax'))
    model.load_weights(model_path)

    predictions = model.predict(data_x)

    id_and_pred = list(zip(id_list, predictions))
    def get_nugget_prob(list_elem):
        return list_elem[1][1]
    id_and_pred.sort(reverse=True, key=get_nugget_prob)
    id_sorted, pred_sorted = zip(*id_and_pred)

    ##########################
    number_nuggets = 30
    ##########################
    # write predictions on file
    prediction_file = open('data/predictions_cnn/nuggets_' + str(topic_number) + '.txt', mode='a')
    for i in range(number_nuggets):
        prediction_file.write(id_sorted[i] + '\t' + sentence_dict[id_sorted[i]])

write_predictions(1001)
