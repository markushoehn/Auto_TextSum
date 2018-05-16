import tensorflow as tf
import numpy as np

# load data
id_train = np.load('data/numpy_data/id_train2.npy')
x_train = np.load('data/numpy_data/x_train2.npy')
y_train = np.load('data/numpy_data/y_train2.npy')
id_test = np.load('data/numpy_data/id_test2.npy')
x_test = np.load('data/numpy_data/x_test2.npy')
y_test = np.load('data/numpy_data/y_test2.npy')
dictionary = np.load('data/numpy_data/dictionary2.npy').item()

# define hyper parameters
batch_size = 10
learning_rate = 0.005
no_epochs = 50
layer_dimensions = [100, 50, 2]
optimizer = tf.train.AdamOptimizer
no_layers = len(layer_dimensions)
layers = [None] * no_layers
activation_functions = [tf.nn.sigmoid] * no_layers

# print hyper parameter setup
print('Hyper parameter setup:\n', 'Batch size =', batch_size, ';', 'Learning rate =', learning_rate, ';',
      'Number of epochs =', no_epochs, ';', 'Network structure =', layer_dimensions, '\n',
      'Optimizer =', optimizer, '\n')

# placeholders for id, input and output data
ids = tf.placeholder(tf.float32, [None, 2])
x = tf.placeholder(tf.float32, [None, 100])
y = tf.placeholder(tf.float32, [None, 2])

# input layer
layers[0] = tf.layers.dense(inputs=x, units=layer_dimensions[0], activation=activation_functions[0],
                            kernel_initializer=tf.random_normal_initializer,
                            bias_initializer=tf.random_normal_initializer)
# hidden layers
if no_layers > 2:
    for layer in range(1, no_layers - 1):
        layers[layer] = tf.layers.dense(inputs=layers[layer - 1], units=layer_dimensions[layer],
                                        activation=activation_functions[layer],
                                        kernel_initializer=tf.random_normal_initializer,
                                        bias_initializer=tf.random_normal_initializer)
# output layer
layers[no_layers - 1] = tf.layers.dense(inputs=layers[no_layers - 2], units=layer_dimensions[no_layers - 1],
                                        activation=activation_functions[no_layers - 1],
                                        kernel_initializer=tf.random_normal_initializer,
                                        bias_initializer=tf.random_normal_initializer)
prediction = layers[no_layers - 1]

# define loss, optimizer and accuracy
# TODO: try different loss functions (cross entropy loss with softmax)
loss = tf.reduce_sum(tf.square(y - prediction))
# loss = tf.nn.softmax_cross_entropy_with_logits_v2(labels=y, logits=prediction)
opt = optimizer(learning_rate=learning_rate).minimize(loss=loss)
accuracy = tf.reduce_mean(tf.cast(tf.equal(y, tf.round(prediction)), 'float'))
# compute F1 score
argmax_prediction = tf.argmax(prediction, 1)
argmax_y = tf.argmax(y, 1)

tp = tf.count_nonzero(argmax_prediction * argmax_y, dtype=tf.float32)
tn = tf.count_nonzero((argmax_prediction - 1) * (argmax_y - 1), dtype=tf.float32)
fp = tf.count_nonzero(argmax_prediction * (argmax_y - 1), dtype=tf.float32)
fn = tf.count_nonzero((argmax_prediction - 1) * argmax_y, dtype=tf.float32)
precision = tp / (tp + fp)
recall = tp / (tp + fn)
f1 = 2 * precision * recall / (precision + recall)

# begin session
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    N = x_train.shape[0]
    # run epochs
    for current_epoch in range(no_epochs):
        # save current loss
        epoch_loss = 0
        no_update_steps = int(np.floor(N / batch_size))
        for current_update in range(no_update_steps):
            # shuffle data
            indices = np.random.choice(N, batch_size)
            x_batch, y_batch = x_train[indices], y_train[indices]
            _, step_loss = sess.run([opt, loss], feed_dict={x: x_batch, y: y_batch})
            epoch_loss += step_loss
        # print training progress
        print('Loss on training data after epoch', current_epoch + 1, ':', np.round(epoch_loss, 2))

    # results
    loss_train, acc_train, prec_train, rec_train, f1_train = sess.run([loss, accuracy, precision, recall, f1],
                                                                      feed_dict={x: x_train, y: y_train})
    loss_test, acc_test, prec_test, rec_test, f1_test = sess.run([loss, accuracy, precision, recall, f1],
                                                                 feed_dict={x: x_test, y: y_test})
    # print results
    print('\nTraining data: Loss =', loss_train, ';', 'Accuracy =', acc_train,
          ';', 'Precision =', prec_train, ';', 'Recall =', rec_train, ';', 'F1 score = ', f1_train)
    print('Test data: Loss =', loss_test, ';', 'Accuracy =', acc_test,
          ';', 'Precision =', prec_test, ';', 'Recall =', rec_test, ';', 'F1 score = ', f1_test)
