import tensorflow as tf
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras import backend as K


def tp(y_true, y_pred):
    return tf.count_nonzero(tf.argmax(y_true, 1) * tf.argmax(y_pred, 1))


def fp(y_true, y_pred):
    return tf.count_nonzero((tf.argmax(y_true, 1) - 1) * tf.argmax(y_pred, 1))


def tn(y_true, y_pred):
    return tf.count_nonzero((tf.argmax(y_true, 1) - 1) * (tf.argmax(y_pred, 1) - 1))


def fn(y_true, y_pred):
    return tf.count_nonzero(tf.argmax(y_true, 1) * (tf.argmax(y_pred, 1) - 1))


'''
def recall(y_true, y_pred):
    # only computes a batch-wise average of recall
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    rec = true_positives / (possible_positives + K.epsilon())
    return rec


def precision(y_true, y_pred):
    # only computes a batch-wise average of precision
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    prec = true_positives / (predicted_positives + K.epsilon())
    return prec


def f1(y_true, y_pred):
    prec = precision(y_true, y_pred)
    rec = recall(y_true, y_pred)
    return 2*((prec*rec)/(prec+rec+K.epsilon()))
'''

# load data
id_train = np.load('data/numpy_data/id_train.npy')
x_train = np.load('data/numpy_data/x_train100_5.npy')
y_train = np.load('data/numpy_data/y_train100_5.npy')
id_test = np.load('data/numpy_data/id_test.npy')
x_test = np.load('data/numpy_data/x_test100_5.npy')
y_test = np.load('data/numpy_data/y_test100_5.npy')
dictionary = np.load('data/numpy_data/dictionary.npy').item()
size_training = x_train.shape[0]
size_testing = x_test.shape[0]

# define hyper parameters
batch_size = 10
number_epochs = 30

# define keras model
model = Sequential()
model.add(Dense(units=50, input_dim=100))
model.add(Activation('relu'))
model.add(Dense(units=2))
model.add(Activation('softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=[tp, fp, tn, fn])
model.fit(x_train, y_train, epochs=number_epochs, batch_size=batch_size)
loss_and_metrics = model.evaluate(x_test, y_test, batch_size=2000)
true_pos = loss_and_metrics[1]
false_pos = loss_and_metrics[2]
true_neg = loss_and_metrics[3]
false_neg = loss_and_metrics[4]
precision = true_pos / (true_pos + false_pos)
recall = true_pos / (true_pos + false_neg)
f1_score = 2 * precision * recall / (precision + recall)
test_prediction = model.predict(x_test)
print('Evaluation:',
      '\n\tLoss:', loss_and_metrics[0],
      '\n\tPrecision:', precision,
      '\n\tRecall:', recall,
      '\n\tF1_Score:', f1_score)
'''
# print nuggets
nugget_count_test = 0
for k in range(size_testing):
    if int(np.argmax(test_prediction[k])) == 1:
        nugget_count_test += 1
        id_string = str(int(id_test[k][0])) + '/' + str(int(id_test[k][1]))
        print(dictionary[id_string])

print('Total nuggets on test data:', nugget_count_test,
      'Nugget ratio on test data:', nugget_count_test / size_testing)
'''
