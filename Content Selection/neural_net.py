import tensorflow as tf
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.callbacks import ModelCheckpoint, EarlyStopping

# METRIC FUNCTIONS FOR LATER EVALUATION (TRUE POSITIVES, FALSE POSITIVES, TRUE NEGATIVES, FALSE NEGATIVES)
def tp(y_true, y_pred):
    return tf.count_nonzero(tf.argmax(y_true, 1) * tf.argmax(y_pred, 1))
def fp(y_true, y_pred):
    return tf.count_nonzero((tf.argmax(y_true, 1) - 1) * tf.argmax(y_pred, 1))
def fn(y_true, y_pred):
    return tf.count_nonzero(tf.argmax(y_true, 1) * (tf.argmax(y_pred, 1) - 1))
def precision(y_true, y_pred):
    tpos = tp(y_true, y_pred)
    fpos = fp(y_true, y_pred)
    return tpos / (tpos + fpos)
def recall(y_true, y_pred):
    tpos = tp(y_true, y_pred)
    fneg = fn(y_true, y_pred)
    return tpos / (tpos + fneg)
def f1_score(y_true, y_pred):
    p = precision(y_true, y_pred)
    r = recall(y_true, y_pred)
    return 2 * p * r / (p + r)


# load data directly as numpy arrays
x_train = np.load('data/numpy_data/x_train_wsize_4_embsize_300.npy')
y_train = np.load('data/numpy_data/y_train_wsize_4_embsize_300.npy')
x_test = np.load('data/numpy_data/x_test_wsize_4_embsize_300.npy')
y_test = np.load('data/numpy_data/y_test_wsize_4_embsize_300.npy')
train_size = x_train.shape[0]
test_size = x_test.shape[0]
# window size
k = 4
# embedding size
emb_size = 300

def train_model(batch_size, number_epoch)

# define hyper parameters of NN
batch_size = 20
number_epochs = 50
optimizer = 'adam'
# dropout rate: ratio of weights which are randomly set inactive for one epoch (prevent overfitting)
dropout_rate = 0.2

# define keras model and NN architecture
model = Sequential()
model.add(Dense(units=100, input_dim=(2*k+1)*emb_size))
model.add(Dropout(dropout_rate))
model.add(Activation('relu'))
model.add(Dense(units=100))
model.add(Dropout(dropout_rate))
model.add(Activation('relu'))
model.add(Dense(units=2))
model.add(Activation('softmax'))

# add early stopping
best_model_path = 'best_model.hdf5'
callbacks = [ModelCheckpoint(filepath=best_model_path, monitor='val_loss', save_best_only=True),
             EarlyStopping(monitor='val_loss', patience=5)]
# specify
model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy', precision, recall, f1_score])
model.fit(x_train, y_train, epochs=number_epochs, batch_size=batch_size, validation_data=(x_test, y_test),
          callbacks=callbacks, verbose=2)
# load best model
model.load_weights('best_model.hdf5')
# choose large batch size for evaluating since the metrics are applied batch-wise and then averaged
loss_and_metrics = model.evaluate(x_test, y_test, batch_size=test_size)
# get metrics
[loss, accuracy, precision, recall, f1_score] = loss_and_metrics
#[loss, true_pos, false_pos, true_neg, false_neg, accuracy] = loss_and_metrics
# calculate precision, recall and f1 score
#precision = true_pos / (true_pos + false_pos)
#recall = true_pos / (true_pos + false_neg)
#f1_score = 2 * precision * recall / (precision + recall)
# get predictions
test_prediction = model.predict(x_test)
# print results
print('Evaluation on test set:',
      '\n\tLoss:', loss,
      '\n\tAccuracy:', accuracy,
      '\n\tPrecision:', precision,
      '\n\tRecall:', recall,
      '\n\tF1_Score:', f1_score)

print(test_prediction)