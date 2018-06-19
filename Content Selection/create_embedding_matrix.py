import numpy as np

# load pre-trained embeddings and save them into a matrix and dictionary

embedding_file_path = 'data/glove.6B.300d.txt'
vector_size = 300

target_path_matrix = 'data/embedding_matrix300.npy'
target_path_dictionary = 'data/embedding_dictionary300.npy'

embedding_file = open(embedding_file_path, encoding='utf-8-sig')
embedding_raw_text = embedding_file.read()
embedding_list = embedding_raw_text.split('\n')
if embedding_list[-1] == '':
    embedding_list = embedding_list[:-1]

vocabulary_size = len(embedding_list)
dictionary = {}
emb_matrix = np.zeros((vocabulary_size, vector_size))
for i in range(vocabulary_size):
    current_embedding = embedding_list[i]
    current_embedding_list = current_embedding.split(' ')
    if not len(current_embedding_list) == 301:
        print(len(current_embedding_list))
        print(current_embedding_list)
    # fill dictionary with index
    dictionary[current_embedding_list[0]] = i
    # fill matrix row
    for j in range(vector_size):
        emb_matrix[i][j] = float(current_embedding_list[j + 1])

# append padding and oov token
dictionary['__padding__'] = vocabulary_size
dictionary['__oov__'] = vocabulary_size + 1
# update vocabulary size
vocabulary_size += 2
emb_matrix = np.append(emb_matrix, np.zeros((1, vector_size)), axis=0)
emb_matrix = np.append(emb_matrix, np.random.rand(1, vector_size), axis=0)

# save matrix and dictionary
print(emb_matrix.shape)
print(dictionary['world'])
np.save(target_path_matrix, emb_matrix)
np.save(target_path_dictionary, dictionary)
