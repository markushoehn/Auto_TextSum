from nltk.classify import apply_features
import nltk
import random

data_file = open('data/complete_feature_file_preprocessed_window_size_2.txt', 'r')
data_lines = data_file.read().split('\n')

labeled_sentences = []
for line in data_lines:
    line_split = line.split('\t')
    labeled_sentences.append([line_split[1:6], line_split[6]])

all_words = nltk.FreqDist(w.lower() for w in sentences_labels for sentences_labels in labeled_sentences)

def sentence_features(sentences):


