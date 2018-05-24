from nltk.classify import apply_features
import nltk
import random

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

print(words)

# all_words = nltk.FreqDist(w.lower() for w in sentences_labels[0][2] for sentences_labels in labeled_sentences)

# def sentence_features(sentences):


