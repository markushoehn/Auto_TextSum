import numpy as np
import random
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout


def train_model(batch_size, number_epochs, optimizer, dropout_rate, number_hidden_layers, layer_dimensions,
                activations, k, emb_size):
    # get data
    x_train = np.load('data/numpy_data/x_train_wsize_' + str(k) + '_embsize_300.npy')
    y_train = np.load('data/numpy_data/y_train_wsize_' + str(k) + '_embsize_300.npy')
    x_test = np.load('data/numpy_data/x_test_wsize_' + str(k) + '_embsize_300.npy')
    y_test = np.load('data/numpy_data/y_test_wsize_' + str(k) + '_embsize_300.npy')
    test_size = x_test.shape[0]

    # define keras model and NN architecture
    model = Sequential()
    model.add(Dense(units=layer_dimensions[0], input_dim=(2*k+1)*emb_size))
    model.add(Dropout(dropout_rate))
    model.add(Activation(activations[0]))
    for i in range(1, number_hidden_layers):
        model.add(Dense(units=layer_dimensions[i]))
        model.add(Dropout(dropout_rate))
        model.add(Activation(activations[i]))
    model.add(Dense(units=2))
    model.add(Activation('softmax'))
    model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])
    model.fit(x_train, y_train, epochs=number_epochs, batch_size=batch_size,
              validation_data=(x_test, y_test), verbose=2)
    # choose large batch size for evaluating since the metrics are applied batch-wise and then averaged
    loss_and_metrics = model.evaluate(x_test, y_test, batch_size=test_size)
    # get metrics
    [loss, accuracy] = loss_and_metrics

    # calculate precision and recall
    test_prediction = model.predict(x_test)
    tp, fp, fn = 0, 0, 0
    for i in range(test_size):
        if np.argmax(test_prediction[i]) == 1:
            if y_test[i][1] == 1:
                tp += 1
            else:
                fp += 1
        else:
            if y_test[i][1] == 1:
                fn += 1
    precision, recall = tp / (tp + fp + 10 ** -8), tp / (tp + fn + 10 ** -8)
    f1_score = 2 * precision * recall / (precision + recall + 10 ** -8)

    return model, loss, accuracy, precision, recall, f1_score


def hyper_parameter_opt(number_of_settings):
    best_model_path = 'best_model.hdf5'
    # best evaluation measures
    best_loss, best_acc, best_prec, best_rec, best_f1 = np.inf, 0, 0, 0, 0
    for i in range(1, number_of_settings + 1):
        print('Setting number', i, 'of', number_of_settings, 'running...')
        # create random hyperparameters
        batch_s = random.randint(10, 20)
        epochs = random.randint(3, 5)
        opt = random.choice(['adam', 'sgd', 'adagrad'])
        dropout = random.uniform(0, 0.3)
        number_hl = random.randint(1, 3)
        layer_dim, act = [], []
        for _ in range(number_hl):
            layer_dim.append(random.randint(50, 150))
            act.append(random.choice(['relu', 'tanh']))
        wind_size = random.randint(1, 5)
        emb_size = 300
        # train model
        model, loss, acc, prec, rec, f1 = train_model(batch_s, epochs, opt, dropout, number_hl, layer_dim, act,
                                                      wind_size, emb_size)

        # update best model
        if prec > best_prec:
            model.save(best_model_path)
            best_loss, best_acc, best_prec, best_rec, best_f1 = loss, acc, prec, rec, f1
            print('Updated best model', '\n', 'Loss:', loss, ', Accuracy:', acc, ', Precision:', prec,
                  ', Recall:', rec, ', F1 Score:', f1, '\n',
                  'Batch size:', batch_s, ', Number of epochs:', epochs, ', Optimizer;', opt,
                  ', Dropout rate:', dropout, ', Number of hidden layers:', number_hl,
                  ', Hidden layer dimensions:', layer_dim, ', Activation functions:', act, ', Window size:', wind_size)


hyper_parameter_opt(5)
