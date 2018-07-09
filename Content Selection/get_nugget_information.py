import numpy as np
import nltk
from gensim.utils import simple_preprocess

# get information about nuggets such as
# minimum length, maximum length, average length and contains verb / no verb

# load complete preprocessed data
data_file = open('data/labeled_data_complete.txt')
data_lines = data_file.read().split('\n')

min_length = np.inf
max_length = 0
avg_length = 0
total_number_nuggets = 0
contains_verb_total = 0
contains_no_verb_total = 0
c = 0

# iterate over all sentences
for line in data_lines:
    split_line = line.split('\t')
    # get sentence and label
    nugget, label = split_line[1], split_line[2]
    # check for nugget, e.g. label = 1
    if int(label) == 1:
        # update number of nuggets
        total_number_nuggets += 1
        # tokenize nugget using gensim simple preprocess
        tokens = simple_preprocess(nugget)
        # save length of nugget and sum average
        nugget_length = len(tokens)
        avg_length += nugget_length
        # update minimum and maximum length
        if nugget_length < min_length:
            min_length = nugget_length
        if nugget_length > max_length:
            max_length = nugget_length
        # get POS tags of current sentence
        pos_tags = nltk.pos_tag(tokens, tagset='universal')
        # check for verb in nugget
        contains_verb = False
        for tag in pos_tags:
            if tag[1] == 'VERB':
                contains_verb = True
                break
        # update
        if contains_verb:
            contains_verb_total += 1
        else:
            contains_no_verb_total += 1
# compute average
avg_length = avg_length / total_number_nuggets

# print results
print('Total number of nuggets:', total_number_nuggets, '\n',
      'Minimum nugget length:', min_length, '\n',
      'Maximum nugget length:', max_length, '\n',
      'Average nugget length:', avg_length, '\n',
      'Number of nuggets that contain a verb:', contains_verb_total, '\n',
      'Number of nuggets that contain no verb:', contains_no_verb_total)
