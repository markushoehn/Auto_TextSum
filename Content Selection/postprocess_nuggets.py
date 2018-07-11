from nltk.tokenize import word_tokenize

source_path = '../Pipeline/01_selected_nuggets/nuggets_'
target_path = '../Pipeline/01_selected_nuggets_new/nuggets_'
max_nuggets = 30

bad_tokens = ['I', 'i', '?']

for i in range(1001, 1051):
    if not i == 1009:
        source_file = open(source_path + str(i) + '.txt', mode='r')
        target_file = open(target_path + str(i) + '.txt', mode='a')
        lines = source_file.read().split('\n')
        total_nugget_count = 0
        for line in lines:
            if total_nugget_count < max_nuggets:
                line_split = line.split('\t')
                if len(line_split) > 1:
                    sent_id, sentence = line_split[0], line_split[1]
                    tokens = word_tokenize(sentence)
                    contains_bad_tokens = False
                    for bad_tok in bad_tokens:
                        if bad_tok in tokens:
                            contains_bad_tokens = True
                            break
                    if not contains_bad_tokens:
                        target_file.write(sent_id + '\t' + sentence + '\n')
                    total_nugget_count += 1
