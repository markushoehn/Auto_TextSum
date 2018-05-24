from nltk.classify import apply_features
from nltk import precision
from nltk import recall
import nltk
import random
import collections
import numpy as np

data_file = open('data/complete_feature_file_preprocessed_window_size_2.txt', 'r')
data_lines = data_file.read().split('\n')

# window size
k = 2

labeled_sentences = []
words = []
for line in data_lines:
    line_split = line.split('\t')
    labeled_sentences.append([line_split[1:6], line_split[6]])
    word_list = line_split[k + 2].split(' ')
    for word in word_list:
        words.append(word)


all_words = nltk.FreqDist(words)
# take most frequent words
word_features = list(all_words)[:10]

embedding_matrix = np.load('data/embedding_matrix.npy')
embedding_dict = np.load('data/embedding_dictionary.npy').item()


def average_embedding(sentence):
    word_list = sentence.split(' ')
    sentence_length = len(word_list)
    embeddings = np.zeros((sentence_length, 50))
    for i in range(sentence_length):
        try:
            embeddings[i] = embedding_matrix[embedding_dict[word_list[i].lower()]]
        except KeyError:
            embeddings[i] = embedding_matrix[embedding_dict['__oov__']]
    return np.mean(embeddings, axis=0)


def sentence_features(sentences):
    number_of_sentences = len(sentences)
    sentence_words = set(sentences[k + 1])
    features = {}
    for word in word_features:
        features['contains({})'.format(word)] = (word in sentence_words)
    # add sentence length as feature (in blocks of 5 words)
    sentence_len = len(sentence_words)
    sentence_len_mod_5 = sentence_len % 5
    sentence_len_discr = str(sentence_len - sentence_len_mod_5) + ' to ' + str(sentence_len - sentence_len_mod_5 + 5)
    features['sentence_length'] = sentence_len_discr
    return features


random.shuffle(labeled_sentences)
splitline = int(len(labeled_sentences) * 3/4)
train_sentences = labeled_sentences[:splitline]
test_sentences = labeled_sentences[splitline:]
train_set = apply_features(sentence_features, train_sentences)
test_set = apply_features(sentence_features, test_sentences)

classifier = nltk.NaiveBayesClassifier.train(train_set)

# calculate precision and recall
refsets = collections.defaultdict(set)
testsets = collections.defaultdict(set)

for i, (feats, label) in enumerate(test_set):
    refsets[label].add(i)
    observed = classifier.classify(feats)
    testsets[observed].add(i)

print('Precision:', precision(refsets['1'], testsets['1']))
print('Recall:', recall(refsets['1'], testsets['1']))

print(nltk.classify.accuracy(classifier, test_set))
classifier.show_most_informative_features(10)
