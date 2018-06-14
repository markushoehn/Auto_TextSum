import gensim

complete_labeled_data_file = open('data/labeled_data_complete.txt', 'r')
complete_list = complete_labeled_data_file.readlines()
number_instances = len(complete_list)

# window size
k = 5

# load stopword list
stopword_file = open('data/stopwords.txt', 'r')
stopword_list = stopword_file.read().split('\n')

# create raw and preprocessed feature file
feature_file_raw = open('data/complete_feature_file_raw_window_size_' + str(k) + '.txt', 'a')
feature_file_preprocessed = open('data/complete_feature_file_preprocessed_window_size_' + str(k) + '.txt', 'a')

for i in range(number_instances):
    current_line_split = complete_list[i].split('\t')
    current_id = current_line_split[0]
    current_label = current_line_split[2]
    # get document id of current line
    doc_id_current_line = '/'.join(current_id.split('/')[0:2])

    window = ''
    window_preprocessed = ''

    # iterate over complete window
    for j in range(i - k, i + k + 1):
        # check for left or right global margin
        if j < 0 or j > number_instances - 1:
            window += '__PADDING__\t'
            window_preprocessed += '__PADDING__\t'
        else:
            # check if sentence is in current document
            doc_id_temp = '/'.join(complete_list[j].split('\t')[0].split('/')[0:2])
            if doc_id_temp == doc_id_current_line:
                # append to original window
                window += complete_list[j].split('\t')[1] + '\t'
                # append to preprocess window
                preprocessed_sentence_tokens = gensim.utils.simple_preprocess(complete_list[j].split('\t')[1])
                preprocessed_sentence = ' '.join([token for token in preprocessed_sentence_tokens
                                                  if token not in stopword_list])
                window_preprocessed += preprocessed_sentence + '\t'
            else:
                window += '__PADDING__\t'
                window_preprocessed += '__PADDING__\t'

    new_line_raw = current_id + '\t' + window + current_label
    new_line_preprocessed = current_id + '\t' + window_preprocessed + current_label
    # write on new files
    feature_file_raw.write(new_line_raw)
    feature_file_preprocessed.write(new_line_preprocessed)


