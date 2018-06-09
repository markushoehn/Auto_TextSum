import tensorflow as tf
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
import random

# METRIC FUNCTIONS FOR LATER EVALUATION (TRUE POSITIVES, FALSE POSITIVES, TRUE NEGATIVES, FALSE NEGATIVES)


def tp(y_true, y_pred):
    return tf.count_nonzero(tf.argmax(y_true, 1) * tf.argmax(y_pred, 1))


def fp(y_true, y_pred):
    return tf.count_nonzero((tf.argmax(y_true, 1) - 1) * tf.argmax(y_pred, 1))


def tn(y_true, y_pred):
    return tf.count_nonzero((tf.argmax(y_true, 1) - 1) * (tf.argmax(y_pred, 1) - 1))


def fn(y_true, y_pred):
    return tf.count_nonzero(tf.argmax(y_true, 1) * (tf.argmax(y_pred, 1) - 1))


# load data directly as numpy arrays
x_train = np.load('data/numpy_data/x_train_wsize_2_embsize_50.npy')
y_train = np.load('data/numpy_data/y_train_wsize_2_embsize_50.npy')
x_test = np.load('data/numpy_data/x_test_wsize_2_embsize_50.npy')
y_test = np.load('data/numpy_data/y_test_wsize_2_embsize_50.npy')

# define hyper parameters of NN
batch_size = 20
number_epochs = 10
optimizer = 'adam'
# dropout rate: ratio of weights which are randomly set inactive for one epoch (prevent overfitting)
dropout_rate = 0.2

# define keras model and NN architecture
model = Sequential()
model.add(Dense(units=100, input_dim=250))
model.add(Dropout(dropout_rate))
model.add(Activation('relu'))
model.add(Dense(units=100))
model.add(Dropout(dropout_rate))
model.add(Activation('relu'))
model.add(Dense(units=2))
model.add(Activation('softmax'))

# specify
model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=[tp, fp, tn, fn, 'accuracy'])
model.fit(x_train, y_train, epochs=number_epochs, batch_size=batch_size)
# choose large batch size for evaluating since the metrics are applied batch-wise and then averaged
loss_and_metrics = model.evaluate(x_test, y_test, batch_size=2000)
# get metrics
[loss, true_pos, false_pos, true_neg, false_neg, accuracy] = loss_and_metrics
# calculate precision, recall and f1 score
precision = true_pos / (true_pos + false_pos)
recall = true_pos / (true_pos + false_neg)
f1_score = 2 * precision * recall / (precision + recall)
# get predictions
test_prediction = model.predict(x_test)
# print results
print('Evaluation on test set:',
      '\n\tLoss:', loss,
      '\n\tAccuracy:', accuracy,
      '\n\tPrecision:', precision,
      '\n\tRecall:', recall,
      '\n\tF1_Score:', f1_score)
