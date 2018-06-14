from keras.models import Sequential
from keras.callbacks import ModelCheckpoint, EarlyStopping
from keras.layers import *
from keras.layers.normalization import BatchNormalization
import numpy as np
import random


# load data
x_train, y_train = np.load('data/numpy_data/x_train_cnn300.npy'), np.load('data/numpy_data/y_train_cnn300.npy')
x_dev, y_dev = np.load('data/numpy_data/x_dev_cnn300.npy'), np.load('data/numpy_data/y_dev_cnn300.npy')
x_test, y_test = np.load('data/numpy_data/x_test_cnn300.npy'), np.load('data/numpy_data/y_test_cnn300.npy')
train_size, dev_size, test_size = x_train.shape[0], x_dev.shape[0], x_test.shape[0]

embedding_dims = 300
pad_length = 50
patience = 2
train_verbose = 1
# load embedding matrix
emb_matrix = np.load('data/numpy_data/embedding_matrix300.npy')
vocab_size = emb_matrix.shape[0]


def train_model(batch_size, optimizer, number_conv_layers, number_filters, kernel_sizes, acts):
    best_model_path_early_stopping = 'best_model_cnn_early_stopping.hdf5'

    model_earling_stopping = Sequential()
    model_earling_stopping.add(Embedding(vocab_size, embedding_dims, weights=[emb_matrix], input_length=pad_length))
    model_earling_stopping.add(BatchNormalization())
    for i in range(number_conv_layers):
        model_earling_stopping.add(Conv1D(filters=number_filters[i], kernel_size=kernel_sizes[i]))
        model_earling_stopping.add(Activation(acts[i]))
    model_earling_stopping.add(GlobalMaxPool1D())
    model_earling_stopping.add(Dense(units=2))
    model_earling_stopping.add(Activation('softmax'))
    model_earling_stopping.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])
    # add model checkpoint and early stopping
    callbacks = [ModelCheckpoint(filepath=best_model_path_early_stopping, monitor='val_loss', save_best_only=True),
                 EarlyStopping(monitor='val_loss', patience=patience)]
    model_earling_stopping.fit(x_train, y_train, batch_size=batch_size, epochs=100, verbose=train_verbose,
                               validation_data=(x_dev, y_dev), callbacks=callbacks)
    # load best model
    model_earling_stopping.load_weights(filepath=best_model_path_early_stopping)
    loss_and_metrics = model_earling_stopping.evaluate(x_test, y_test, batch_size=dev_size, verbose=0)
    loss, accuracy = loss_and_metrics[0], loss_and_metrics[1]
    prediction = model_earling_stopping.predict(x_test)
    # calculate precision, recall and f1 score
    tp, fp, fn = 0, 0, 0
    for i in range(test_size):
        if np.argmax(prediction[i]) == 1:
            if y_test[i][1] == 1:
                tp += 1
            else:
                fp += 1
        else:
            if y_test[i][1] == 1:
                fn += 1
    precision, recall = tp / (tp + fp + 10 ** -8), tp / (tp + fn + 10 ** -8)
    f1_score = 2 * precision * recall / (precision + recall + 10 ** -8)
    return model_earling_stopping, loss, accuracy, precision, recall, f1_score


def hyper_parameter_opt(number_of_settings):
    best_model_path = 'best_model_cnn.hdf5'
    # best evaluation measures
    best_loss, best_acc, best_prec, best_rec, best_f1 = np.inf, 0, 0, 0, 0
    for i in range(1, number_of_settings + 1):
        print('Setting number', i, 'of', number_of_settings, 'running...')
        # create random hyperparameters
        batch_s = random.randint(100, 150)
        opt = random.choice(['adam', 'sgd', 'adagrad'])
        number_cl = random.randint(1, 2)
        filters, kernel_s, act = [], [], []
        for _ in range(number_cl):
            filters.append(random.randint(30, 60))
            kernel_s.append(random.randint(3, 7))
            act.append(random.choice(['relu', 'tanh']))
        # train model
        model, loss, acc, prec, rec, f1 = train_model(batch_s, opt, number_cl, filters, kernel_s, act)

        # update best model
        if prec > best_prec:
            model.save(best_model_path)
            best_loss, best_acc, best_prec, best_rec, best_f1 = loss, acc, prec, rec, f1
            print('Updated best model', '\n', 'Loss:', loss, ', Accuracy:', acc, ', Precision:', prec,
                  ', Recall:', rec, ', F1 Score:', f1, '\n',
                  'Batch size:', batch_s, ', Optimizer;', opt, ', Number of convolutional layers:', number_cl,
                  ', Number of filters:', filters, ', Kernel sizes:', kernel_s,
                  ', Activation functions:', act)


hyper_parameter_opt(5)
