

source_path = '../Pipeline/01_selected_nuggets/nuggets_'
target_path = '../Pipeline/01_selected_nuggets_new/nuggets_'
max_nuggets = 30

for i in range(1001, 1051):
    if not i == 1009:
        source_file = open(source_file + str(i) + '.txt')
        lines = source_file.read().split('\n')
        for line in lines:
            sent_id, sentence = line.split('\t')
