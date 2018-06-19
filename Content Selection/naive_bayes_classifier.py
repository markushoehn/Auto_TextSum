from nltk.classify import apply_features
import nltk
import random

data_file = open('data/complete_feature_file_preprocessed_window_size_2.txt', 'r')
data_lines = data_file.read().split('\n')

# window size
k = 2

# create dictionary for raw data
raw_data_dict = {}
raw_data = ['data/unlabeled/raw/unlabeled_raw_10' + str(format(i, '02d')) + '.txt' for i in range(1, 50)]
for content_number in range(1, 50):
    # number 9 is missing
    if not content_number == 9:
        source_file = open(raw_data[content_number - 1], 'r')
        source_list = source_file.read().split('\n')
        # loop over lines
        for line in source_list:
            split_line = line.split('\t')
            current_id = split_line[0]
            current_raw_sentence = split_line[1]
            # write in dictionary
            raw_data_dict[current_id] = current_raw_sentence

# create labeled sentences: list of ([[doc_id, [sentence1,...,sentence2k+1]], label])
labeled_sentences = []
words = []
for line in data_lines:
    line_split = line.split('\t')
    labeled_sentences.append([[line_split[0], line_split[1:6]], line_split[6]])
    word_list = line_split[k + 2].split(' ')
    for word in word_list:
        words.append(word)


# extract number of sentences for each document and content vocabulary over all (unlabeled) data
number_of_sentences_in_doc = {}
vocabulary = {}
word_features = {}
unlabeled_data = ['data/unlabeled/preprocessed/unlabeled_preprocessed_10' + str(format(i, '02d')) + '.txt'
                  for i in range(1, 50)]
for content_number in range(1, 50):
    # document 9 is missing
    if not content_number == 9:
        # read file
        current_file = open(unlabeled_data[content_number - 1])
        current_file_list = current_file.read().split('\n')
        # create placeholder for word list
        words_in_current_doc = []
        # loop over all sentences
        for line in current_file_list:
            # split line
            split_line = line.split('\t')
            # get id and sentence
            current_id = split_line[0]
            sentence = split_line[1]
            # remove sentence id
            doc_id = '/'.join(current_id.split('/')[0:2])
            # count sentence up
            if doc_id in number_of_sentences_in_doc:
                number_of_sentences_in_doc[doc_id] += 1
            else:
                number_of_sentences_in_doc[doc_id] = 1
            # add words in sentence to words in current document
            words_in_sentence = sentence.split(' ')
            for word in words_in_sentence:
                words_in_current_doc.append(word)
        content_id = '10' + str(format(content_number, '02d'))
        vocabulary[content_id] = words_in_current_doc
        all_words = nltk.FreqDist(words_in_current_doc)
        number_of_most_freq_words = 10
        word_features[content_id] = list(all_words)[:number_of_most_freq_words]

# SPECIFY SENTENCE FEATURES


def sentence_features(id_and_sentences):
    id_of_sentence = id_and_sentences[0]
    id_split = id_of_sentence.split('/')
    # get topic id, document id and sentence id
    topic_id = id_split[0]
    doc_id = topic_id + '/' + id_split[1]
    sentence_id = id_split[2]
    sentences = id_and_sentences[1]
    # only look at the middle (actual) sentence for the moment
    sentence_words = set(sentences[k])

    # create features for most topic specific words
    features = {}
    for word in word_features[topic_id]:
        features['contains({})'.format(word)] = (word in sentence_words)

    # add position in document as feature (blockwise)
    rel_pos_in_doc = int(sentence_id) / number_of_sentences_in_doc[doc_id]
    # discretize
    disc_step = 6
    pos_in_doc_discr = int(10 * rel_pos_in_doc) % disc_step
    features['pos_in_doc'] = pos_in_doc_discr

    # add sentence length as feature (in blocks of n words)
    n = 2
    sentence_len = len(sentence_words)
    sentence_len_mod = sentence_len % n
    sentence_len_discr = str(sentence_len - sentence_len_mod) + ' to ' + str(sentence_len - sentence_len_mod + n)
    features['sentence_length'] = sentence_len_discr

    # pos tagging for further features (work with raw text)
    raw_sentence = raw_data_dict[id_of_sentence]
    # get pos tags
    pos_tags = nltk.pos_tag(nltk.word_tokenize(raw_sentence))
    contains_verb = 0
    for (token, pos_tag) in pos_tags:
        if pos_tag in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']:
            contains_verb = 1
            break
    features['contains_verb'] = contains_verb
    return features


# shuffle data and split into training and testing data
random.shuffle(labeled_sentences)
splitline = int(len(labeled_sentences) * 3/4)
train_sentences = labeled_sentences[:splitline]
test_sentences = labeled_sentences[splitline:]
train_set = apply_features(sentence_features, train_sentences)
test_set = apply_features(sentence_features, test_sentences)

classifier = nltk.NaiveBayesClassifier.train(train_set)
classifier.show_most_informative_features(20)

# evaluating: print errors and calculate precision and recall
errors = []
tp = 0
fp = 0
tn = 0
fn = 0
for (sentences, tag) in test_sentences:
    guess = classifier.classify(sentence_features(sentences))
    if guess != tag:
        errors.append((tag, guess, sentences[1][2]))
    if guess == '1':
        if tag == '1':
            tp += 1
        else:
            fp += 1
    else:
        if tag == '1':
            fn += 1
        else:
            tn += 1
try:
    precision = tp / (tp + fp)
except ZeroDivisionError:
    precision = None
try:
    recall = tp / (tp + fn)
except ZeroDivisionError:
    recall = None
try:
    f1_score = 2 * precision * recall / (precision + recall)
except TypeError:
    f1_score = None
print('True positives:', tp, 'False positives:', fp, 'True negatives;', tn, 'False negatives:', fn)
print('Precision:', precision, 'Recall:', recall, 'F1 Score:', f1_score)

for (tag, guess, sentence) in sorted(errors):
    print('correct={:<3} guess={:<3} sentence={:<30}'.format(tag, guess, sentence))
