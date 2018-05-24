import gensim

# parameters
min_count = 1
window_size = 5
vec_dim = 100

sentences = gensim.models.word2vec.LineSentence('data/word2vec_training_data.txt')
model = gensim.models.Word2Vec(sentences, size=vec_dim, window=window_size, min_count=min_count)
model.save('data/word2vec_embeddings_dim100_window5.vec')