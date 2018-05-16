
label_file = open('data/nugget_metdata_results/data_labels.txt', 'r')
label_file_text = label_file.read()
label_file_textlines = label_file_text.split('\n')

doc_number_of_sentences = [1475, 902, 2586, 3119, 2346, 6183, 6409, 1209, 7654, 3916]
doc_ids = ['1001', '1002', '1006', '1016', '1017', '1029', '1030', '1035', '1042', '1044']

label_new_file = open('data/nugget_metdata_results/data_labels_with_ids.txt', 'w')

k = 0
for i in range(0, 10):
    for j in range(doc_number_of_sentences[i]):
        label_new_file.write(doc_ids[i] + '/' + str(j) + '\t' + label_file_textlines[k + j] + '\n')
    k += doc_number_of_sentences[i]
