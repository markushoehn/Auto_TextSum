from gensim.utils import simple_preprocess
from nltk.tokenize import word_tokenize

source_file = open('data/labeled_data_complete.txt', 'r')
lines = source_file.read().split('\n')

relevant_phrases = [' is a ', ' is an ', ' is the ', ' was a ', ' was an ', ' is one of ', ' also known as ',
                    ' are a ', ' are some ', 'one of the']

non_relevant_phrases = [' in my opinion ', ' he ', ' she ', ' we ', ' her ', ' his ']

nugget_count = 0
no_nugget_count = 0

for line in lines:
    sent_id, sentence, label = line.split('\t')
    sentence_preprocessed = simple_preprocess(sentence)
    if 5 <= len(sentence_preprocessed) <= 50:
        tokens = word_tokenize(sentence)
        if 'i' not in tokens and 'I' not in tokens and '?' not in tokens and 'we' not in tokens and 'We' not in tokens:
            sentence_preprocessed = ' '.join(sentence_preprocessed)
            has_rel_phrase = False
            for phrase in relevant_phrases:
                if phrase in sentence_preprocessed:
                    has_rel_phrase = True
                    break
            has_non_rel_phrase = False
            for phrase in non_relevant_phrases:
                if phrase in sentence_preprocessed:
                    has_non_rel_phrase = True
                    break
            if has_rel_phrase and not has_non_rel_phrase:
                if int(label) == 1:
                    nugget_count += 1
                elif int(label) == 0:
                    no_nugget_count += 1
                print('Sentence ID:', sent_id, '\n\t', sentence, '\n', 'Label:', label)

print('\n', 'Nuggets:', nugget_count, ', no nuggets:', no_nugget_count)
