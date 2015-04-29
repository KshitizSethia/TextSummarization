from gensim.models.word2vec import Word2Vec
import os
import settings

model = Word2Vec()
model.save(settings.word2vecModel)

for corpus in os.listdir(settings.corpus_folder):
    filename = os.path.join(settings.corpus_folder, corpus)
    model = model.load(settings.word2vecModel)
    model.build_vocab(open(filename, "r"))
    model.train(open(filename, "r"))
    model.save(settings.word2vecModel)