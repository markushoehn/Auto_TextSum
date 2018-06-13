from keras.models import Sequential, Model
from keras.callbacks import ModelCheckpoint, EarlyStopping
from keras.layers import *
from keras.layers.normalization import BatchNormalization
import numpy as np


# load data
x_train, y_train = np.load('data/numpy_data/x_train_cnn300.npy'), np.load('data/numpy_data/y_train_cnn300.npy')
x_dev, y_dev = np.load('data/numpy_data/x_dev_cnn300.npy'), np.load('data/numpy_data/y_dev_cnn300.npy')
x_test, y_test = np.load('data/numpy_data/x_test_cnn300.npy'), np.load('data/numpy_data/y_test_cnn300.npy')
train_size, dev_size, test_size = x_train.shape[0], x_dev.shape[0], x_test.shape[0]

# load embedding matrix
emb_matrix = np.load('data/embedding_matrix300.npy')
vocab_size = emb_matrix.shape[0]

# hyper parameters
batch_size = 256
embedding_dims = 300
epochs = 50
filters = 50
kernel_size = 5
train_verbose = 2
pad_length = 50
patience = 2
best_model_path = 'best_model.hdf5'

model_earling_stopping = Sequential()
model_earling_stopping.add(Embedding(vocab_size, embedding_dims, weights=[emb_matrix], input_length=pad_length))
model_earling_stopping.add(BatchNormalization())
model_earling_stopping.add(Conv1D(filters=filters, kernel_size=kernel_size))
model_earling_stopping.add(Activation('relu'))
model_earling_stopping.add(Conv1D(filters=filters, kernel_size=kernel_size))
model_earling_stopping.add(Activation('relu'))
model_earling_stopping.add(GlobalMaxPool1D())
model_earling_stopping.add(Dense(units=2))
model_earling_stopping.add(Activation('softmax'))
model_earling_stopping.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
# add model checkpoint and early stopping
callbacks = [ModelCheckpoint(filepath=best_model_path, monitor='val_loss', save_best_only=True),
             EarlyStopping(monitor='val_loss', patience=patience)]
model_earling_stopping.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, verbose=train_verbose,
                           validation_data=(x_dev, y_dev), callbacks=callbacks)
# load best model
model_earling_stopping.load_weights(filepath=best_model_path)
loss_and_metrics = model_earling_stopping.evaluate(x_dev, y_dev, batch_size=dev_size, verbose=0)
print(loss_and_metrics)
prediction = model_earling_stopping.predict(x_dev)
# calculate precision, recall and f1 score
tp, fp, fn = 0, 0, 0
count_real = 0
for i in range(dev_size):
    if np.argmax(prediction[i]) == 1:
        if y_dev[i][1] == 1:
            tp += 1
        else:
            fp += 1
    else:
        if y_dev[i][1] == 1:
            fn += 1
    if y_dev[i][1] == 1:
        count_real += 1
precision, recall = tp / (tp + fp + 10**-8), tp / (tp + fn + 10**-8)
f1_score = 2 * precision * recall / (precision + recall + 10**-8)
print('Precision:', precision, 'Recall:', recall, 'F1 Score:', f1_score)
print('Predicted positives and ratio:', tp, tp / dev_size)
print('Real positives and ratio:', count_real, count_real/dev_size)
